from websocket import create_connection


def get_api_data(url):
    """
    !!! param TOKEN will be replace true api token !!!
    :param url: https://apifootball.com/api/?APIkey=TOKEN&action=get_standings&league_id=63
    :return: result type str
    """
    ws = create_connection("ws://34.91.248.129:7351/")
    ws.send(url)
    result = ws.recv()
    ws.close()
    return result
