from config import default_config
import futuquant as ft


class Futu_Opend:
    def __init__(self, ):
        self.quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,
                                             port=default_config.FUTU_OPEND_PORT)

    def close(self):
        self.quote_ctx.close()

    def subscribe(self, code_list):
        self.quote_ctx.subscribe(code_list, [ft.SubType.QUOTE])

    def unsubscribe_all(self):
        state, sub_data = self.quote_ctx.query_subscription()
        if sub_data["total_used"] > 0:
            self.quote_ctx.unsubscribe(sub_data["sub_list"]["QUOTE"], [ft.SubType.QUOTE])

futu_opend = Futu_Opend()
