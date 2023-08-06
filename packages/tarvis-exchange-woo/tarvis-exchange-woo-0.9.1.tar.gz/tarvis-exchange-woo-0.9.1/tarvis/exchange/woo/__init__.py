from decimal import Decimal
from enum import Enum
from tarvis.common import secrets
import tarvis.common.environ
from tarvis.common.environ import DeploymentType
from tarvis.common.trading import Exchange, Order, OrderSide, OrderType, TradingPolicy
from tarvis.exchange.woo.wooclient import WooClient


class WooVersion(Enum):
    SPOT = 0
    MARGIN = 1
    PERPETUAL = 2


class WooExchange(Exchange):
    EXCHANGE_NAME = "Woo"

    _STANDARD_ORDER_TYPE_TO_WOO = {
        OrderType.MARKET: "MARKET",
        OrderType.LIMIT: "LIMIT",
    }
    _STANDARD_ORDER_TYPE_TO_TARVIS = dict(
        (value, key) for key, value in _STANDARD_ORDER_TYPE_TO_WOO.items()
    )
    _STANDARD_TARVIS_ORDER_TYPES = _STANDARD_ORDER_TYPE_TO_WOO.keys()
    _STANDARD_WOO_ORDER_TYPES = _STANDARD_ORDER_TYPE_TO_TARVIS.keys()

    _ALGO_ORDER_TYPE_TO_WOO = {
        OrderType.STOP_LOSS_MARKET: ("STOP", "MARKET"),
    }

    def __init__(
        self,
        credentials_secret: str,
        version: str | WooVersion = WooVersion.SPOT,
    ):
        super().__init__()
        self.stop_loss_orders_supported = True

        if isinstance(version, str):
            version = WooVersion[version.upper()]
        self._version = version

        if version == WooVersion.PERPETUAL:
            self._market_type = "PERP"
        else:
            self._market_type = "SPOT"

        self.short_selling_supported = version in [
            WooVersion.MARGIN,
            WooVersion.PERPETUAL,
        ]

        credentials = secrets.get_secret(credentials_secret, decode_json=True)
        api_key = credentials["api_key"]
        api_secret = credentials["api_secret"]

        if tarvis.common.environ.deployment == DeploymentType.PRODUCTION:
            base_url = "https://api.woo.org/"
        else:
            base_url = "https://api.staging.woo.org/"

        self._client = WooClient(base_url, api_key, api_secret)

    @staticmethod
    def _convert_market_to_assets(market: str) -> (str, str, str):
        market_type, base_asset, quote_asset = market.split("_")
        return market_type, base_asset, quote_asset

    def _convert_assets_to_market(self, base_asset: str, quote_asset: str) -> str:
        return "_".join((self._market_type, base_asset, quote_asset))

    def get_policy(self, base_asset: str, quote_asset: str) -> TradingPolicy:
        market = self._convert_assets_to_market(base_asset, quote_asset)
        exchange_response = self._client.get_public_info(market)
        market_data = exchange_response["info"]

        minimum_order_quantity = Decimal(market_data["base_min"])
        maximum_order_quantity = Decimal(market_data["base_max"])
        quantity_precision = Decimal(market_data["base_tick"])
        price_precision = Decimal(market_data["quote_tick"])
        minimum_order_value = float(market_data["min_notional"])

        return TradingPolicy(
            minimum_order_quantity=minimum_order_quantity,
            minimum_order_value=minimum_order_value,
            maximum_order_quantity=maximum_order_quantity,
            quantity_precision=quantity_precision,
            price_precision=price_precision,
        )

    def get_quote(self, base_asset: str, quote_asset: str) -> Decimal:
        market = self._convert_assets_to_market(base_asset, quote_asset)
        response = self._client.get_kline(market, "1m", 1)
        row = response["rows"][0]
        price = row["close"]
        return Decimal(price)

    def get_positions(self) -> dict[str, Decimal]:
        results = {}

        holding_response = self._client.get_balances()
        holdings = holding_response["data"]["holding"]

        for holding in holdings:
            base_asset = holding["token"]
            quantity = holding["holding"]
            quantity = Decimal(quantity)
            results[base_asset] = quantity

        if self._version == WooVersion.PERPETUAL:
            positions_response = self._client.get_positions()
            positions = positions_response["data"]["positions"]

            for position in positions:
                symbol = position["symbol"]
                quantity = position["holding"]
                price = position["averageOpenPrice"]
                _, base_asset, quote_asset = self._convert_market_to_assets(symbol)
                quantity = Decimal(quantity)
                price = Decimal(price)
                base_quantity = results.get(base_asset, 0)
                quote_quantity = results.get(quote_asset, 0)
                results[base_asset] = base_quantity + quantity
                results[quote_asset] = quote_quantity - (quantity * price)

        return results

    def _get_open_orders_standard(self) -> list[Order]:
        _PAGE_SIZE = 500

        results = {}
        page_order_count = _PAGE_SIZE
        page = 1
        while page_order_count == _PAGE_SIZE:
            response = self._client.get_orders(
                status="INCOMPLETE", size=_PAGE_SIZE, page=page
            )
            woo_orders = response["rows"]
            page_order_count = len(woo_orders)
            page += 1

            for woo_order in woo_orders:
                symbol = woo_order["symbol"]
                market_type, quote_asset, base_asset = self._convert_market_to_assets(
                    symbol
                )
                order_type = woo_order["type"]

                if (market_type == self._market_type) and (
                    order_type in self._STANDARD_WOO_ORDER_TYPES
                ):
                    order_id = woo_order["order_id"]
                    quantity = woo_order.get("quantity")
                    amount = woo_order.get("amount")
                    price = woo_order.get("price")
                    side = woo_order["side"]
                    creation_time = woo_order["created_time"]
                    filled_quantity = woo_order.get("executed", 0)

                    side = OrderSide[side]
                    order_type = self._STANDARD_ORDER_TYPE_TO_TARVIS[order_type]
                    meta_data = {"order_id": order_id, "order_method": "standard"}

                    order = Order(
                        quote_asset,
                        base_asset,
                        side,
                        order_type,
                        creation_time,
                        quantity=quantity,
                        amount=amount,
                        price=price,
                        filled_quantity=filled_quantity,
                        meta_data=meta_data,
                    )

                    results[order_id] = order

        return list(results.values())

    def _get_open_orders_algo(self) -> list[Order]:
        _PAGE_SIZE = 25

        results = {}
        page_order_count = _PAGE_SIZE
        page = 1
        while page_order_count == _PAGE_SIZE:
            response = self._client.get_algo_orders(
                algo_type="STOP", status="INCOMPLETE", size=_PAGE_SIZE, page=page
            )
            woo_orders = response["data"]["rows"]
            page_order_count = len(woo_orders)
            page += 1

            for woo_order in woo_orders:
                symbol = woo_order["symbol"]
                market_type, quote_asset, base_asset = self._convert_market_to_assets(
                    symbol
                )
                order_type = woo_order["type"]
                if order_type == "MARKET":
                    order_type = OrderType.STOP_LOSS_MARKET
                else:
                    order_type = None

                if (market_type == self._market_type) and (order_type is not None):
                    order_id = woo_order["algoOrderId"]
                    quantity = woo_order.get("quantity", None)
                    amount = woo_order.get("amount", None)
                    price = woo_order["triggerPrice"]
                    side = woo_order["side"]
                    creation_time = woo_order["createdTime"]
                    filled_quantity = woo_order.get("totalExecutedQuantity")

                    side = OrderSide[side]
                    meta_data = {"order_id": order_id, "order_method": "algo"}

                    order = Order(
                        quote_asset,
                        base_asset,
                        side,
                        order_type,
                        creation_time,
                        quantity=quantity,
                        amount=amount,
                        price=price,
                        filled_quantity=filled_quantity,
                        meta_data=meta_data,
                    )

                    results[order_id] = order

        return list(results.values())

    def get_open_orders(self) -> list[Order]:
        return self._get_open_orders_standard() + self._get_open_orders_algo()

    def place_order(
        self,
        policy: TradingPolicy,
        base_asset: str,
        quote_asset: str,
        side: OrderSide,
        order_type: OrderType,
        quantity: Decimal,
        price: Decimal = None,
        stop_loss_price: Decimal = None,
        increasing_position: bool = None,
    ):
        market = self._convert_assets_to_market(base_asset, quote_asset)

        if order_type in self._STANDARD_TARVIS_ORDER_TYPES:
            standard_order = True
            algo_type = None
            woo_order_type = self._STANDARD_ORDER_TYPE_TO_WOO[order_type]
        else:
            standard_order = False
            algo_type, woo_order_type = self._ALGO_ORDER_TYPE_TO_WOO[order_type]

        if order_type == OrderType.STOP_LOSS_MARKET:
            price = str(stop_loss_price)
        elif price is not None:
            price = str(price)

        if increasing_position is not None:
            reduce_only = not increasing_position
        else:
            reduce_only = None

        if standard_order:
            self._client.post_order(
                market,
                side.name,
                woo_order_type,
                order_quantity=str(quantity),
                order_price=price,
                reduce_only=reduce_only,
            )
        else:
            self._client.post_algo_order(
                market,
                side.name,
                algo_type,
                woo_order_type,
                order_quantity=str(quantity),
                trigger_price=price,
                reduce_only=reduce_only,
            )

    def cancel_order(self, order: Order):
        market = self._convert_assets_to_market(order.base_asset, order.quote_asset)
        if order.meta_data["order_method"] == "standard":
            self._client.delete_order(order.meta_data["order_id"], market)
        else:
            self._client.delete_algo_order(order.meta_data["order_id"])
