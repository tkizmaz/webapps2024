

import thriftpy2
from thriftpy2.rpc import make_server

# Load the Thrift file with the module name ending with '_thrift'
timestampHandlerThrift = thriftpy2.load(
    '../timestamphandler.thrift', module_name='timestamphandler_thrift')

# Access the service from the loaded Thrift module
Timestamp = timestampHandlerThrift.TimestampHandlerService

# Define your handler class
class TimestampHandler:
    def getCurrentTimestamp(self):
        from datetime import datetime
        return str(datetime.now())

# Create a Thrift server
if __name__ == '__main__':
    handler = TimestampHandler()
    server = make_server(Timestamp, handler, '127.0.0.1', 9090)
    server.serve()
