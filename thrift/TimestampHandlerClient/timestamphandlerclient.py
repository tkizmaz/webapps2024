import thriftpy2
from thriftpy2.rpc import make_client
from thriftpy2.thrift import TException
# loads ‘calculator.thrift’ as ‘calculator_thrift’ module and
# the code will be generated on the fly
timestampHandlerThrift = thriftpy2.load(
    'thrift/timestamphandler.thrift', module_name='timestamphandler_thrift')
TimestampHandler = timestampHandlerThrift.TimestampHandlerService


def getTimeStampFromServer():
    try:
        client = make_client(TimestampHandler, '127.0.0.1', 9090)
        return client.getCurrentTimestamp()

    except TException as e:
        print(e)


if __name__ == '__main__':
    getTimeStampFromServer()
