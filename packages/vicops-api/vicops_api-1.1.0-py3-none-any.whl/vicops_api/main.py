import requests


class VicopsApi:
    def __init__(self, host: str = "https://vicops.artegoser.ru"):
        self.host = host

    def _getPost(self, url: str, body: object = {}) -> object:
        body["jwt"] = self.jwt

        res = requests.post(f"{self.host}{url}", data=body)

        if res.status_code != 200:
            return {
                "msg": res.json(),
                "status": res.status_code,
                "code": "denied",
            }

        return res.json()

    def _getGet(self, url: str) -> object:
        res = requests.get(f"{self.host}{url}")

        if res.status_code != 200:
            return {
                "msg": res.json(),
                "status": res.status_code,
                "code": "denied",
            }

        return res.json()

    def _checkRespAndAddJWT(self, resp: object) -> object:
        if resp.code != "denied":
            self.jwt = resp.token
        return resp

    def connectJwt(self, jwt: str) -> object:
        self.jwt = jwt

    def register(
        self,
        id: str,
        name: str,
        second_name: str,
        password: str,
        country: str,
        type: str,
        contact: str,
    ) -> object:
        return self._checkRespAndAddJWT(
            self._getPost(
                "/api/register",
                {
                    "id": id,
                    "name": name,
                    "second_name": second_name,
                    "password": password,
                    "country": country,
                    "type": type,
                    "contact": contact,
                },
            )
        )

    def get_error_codes(self) -> object:
        return self._getGet("/api/error_codes")

    def renew_jwt(self) -> object:
        resp = self._getPost("/api/renew_jwt")
        if resp.code != "denied":
            self.jwt = resp.token

        return resp

    def transaction(
        self,
        recipient_id: str,
        amount: float,
        currency_id: str,
        description: str = "",
        type: str = "transfer",
    ) -> object:
        return self._getPost(
            "/api/transaction",
            {
                "recipient_id": recipient_id,
                "amount": amount,
                "currency_id": currency_id,
                "description": description,
                "type": type,
            },
        )

    def getUser(self) -> object:
        return self._getPost("/api/user")

    def getCurrencies(self) -> object:
        return self._getGet("/api/currencies")

    def approveUser(self, user_id: str) -> object:
        return self._getPost(f"/api/approve", {"user_id": user_id})

    def addCurrency(
        self, _id: str, name: str, description: str, type: str, img: str
    ) -> object:
        return self._getPost(
            f"/api/add_currency",
            {
                "_id": _id,
                "name": name,
                "description": description,
                "type": type,
                "img": img,
            },
        )

    def placeOrder(
        self,
        buy_currency_id: str,
        sell_currency_id: str,
        buy_amount: float,
        sell_amount: float,
    ) -> object:
        return self._getPost(
            "/api/place_order",
            {
                "buy_currency_id": buy_currency_id,
                "sell_currency_id": sell_currency_id,
                "buy_amount": buy_amount,
                "sell_amount": sell_amount,
            },
        )

    def getOrders(self) -> object:
        return self._getGet("/api/orders")

    def buyOrder(self, order_id: str) -> object:
        return self._getPost(
            "/api/buy_order",
            {
                "order_id": order_id,
            },
        )

    def getOrdersByCurrency(
        self, buy_currency_id: str, sell_currency_id: str
    ) -> object:
        return self._getGet(
            f"/api/orders-by-currencies/{buy_currency_id}/{sell_currency_id}"
        )

    def getBoughtOrdersByCurrency(
        self, buy_currency_id: str, sell_currency_id: str
    ) -> object:
        return self._getGet(f"/api/bought-orders/{buy_currency_id}/{sell_currency_id}")

    def getOrder(self, order_id: str) -> object:
        return self._getGet(f"/api/orders/{order_id}")

    def getBalances(self) -> object:
        return self._getPost("/api/balances")

    def getTransactions(self) -> object:
        return self._getPost("/api/transactions")

    def login(self, _id: str, password: str) -> object:
        return self._checkRespAndAddJWT(
            self._getPost(
                "/api/login",
                {
                    "_id": _id,
                    "password": password,
                },
            )
        )
