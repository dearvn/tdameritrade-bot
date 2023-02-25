import logging, os, json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from app.worker.tasks import recommend_options_exe

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_recommend_options(request, format=None):
    key = os.environ.get('STOCK_API_KEY')
    if request.META['HTTP_AUTHORIZATION'] == None or key != request.META['HTTP_AUTHORIZATION']:
        return Response('', status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'POST':
        data = request.data

        if 'tickers' in data:
            for ticker in data['tickers']:
                recommend_options_exe.delay(ticker)

        return Response(data, status=status.HTTP_200_OK)

    return Response('', status=status.HTTP_403_FORBIDDEN)