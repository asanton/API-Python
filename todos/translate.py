import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
traductor = boto3.client('translate')

def translate(event, context):
    idReceived=event['pathParameters']['id']
    languaje=event['pathParameters']['languaje']
    print("Recibido peticion de traduccion para id:"+idReceived+" a lenguaje:"+languaje)
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': idReceived
        }
    )
    jsonStr=json.dumps(result['Item'])
    jsonObj=json.loads(jsonStr)
    print("Resultado-->"+jsonStr+" a traducir-->"+jsonObj['text'])
    resultadoTraduccion = traductor.translate_text(Text=jsonObj['text'], SourceLanguageCode="auto", TargetLanguageCode=languaje)
    print('TranslatedText: ' + resultadoTraduccion.get('TranslatedText'))
    print('SourceLanguageCode: ' + resultadoTraduccion.get('SourceLanguageCode'))
    print('TargetLanguageCode: ' + resultadoTraduccion.get('TargetLanguageCode'))
    jsonObj['text']=resultadoTraduccion.get('TranslatedText')
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(jsonObj,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
