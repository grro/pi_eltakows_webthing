from eltako import EltakoWsSensor
from mcplib.server import MCPServer



class EltakoMCPServer(MCPServer):

    def __init__(self, port: int, sensor: EltakoWsSensor):
        super().__init__("windsensor", port)
        self.sensor = sensor

        @self.mcp.tool()
        def get_wind_status() -> str:
            """
            Returns the current wind speed data for various time intervals.
            """

            status = (
                f"1min average: {self.sensor.windspeed_kmh_1min_granularity} km/h, "
                f"30s average: {self.sensor.windspeed_kmh_30sec_granularity} km/h, "
                f"10s average: {self.sensor.windspeed_kmh_10sec_granularity} km/h, "
                f"5s average: {self.sensor.windspeed_kmh_5sec_granularity} km/h, "
                f"Current speed: {self.sensor.windspeed_kmh} km/h"
            )
            return status
