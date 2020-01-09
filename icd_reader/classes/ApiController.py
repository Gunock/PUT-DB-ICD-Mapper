import json
import logging

from flask import Response

from icd_reader import logger
from icd_reader.classes.DbController import DbController
from icd_reader.classes.IcdMapper import IcdMapper
from icd_reader.classes.IcdWikipediaMapper import IcdWikipediaMapper
from icd_reader.classes.MySqlController import MySqlController

logger.initialize()

icd_mapper: IcdMapper
db_controller: DbController
wikipedia_mapper: IcdWikipediaMapper


def load_configuration():
    global icd_mapper
    global db_controller
    global wikipedia_mapper

    with open('resources/configuration.json', 'r') as f:
        configuration = json.load(f)
        logging.info("Loaded configuration from path 'resources/configuration.json'")
    db_controller = MySqlController(
        host=configuration['db-parameters']['host'],
        user=configuration['db-parameters']['user'],
        password=configuration['db-parameters']['password']
    )
    icd_mapper = IcdMapper(
        client_id=configuration['icd-api-credentials']['client-id'],
        client_secret=configuration['icd-api-credentials']['client-secret']
    )
    wikipedia_mapper = IcdWikipediaMapper("resources/codeSpaces.json")


def add_or_update_icd10(request) -> Response:
    global icd_mapper
    global db_controller
    global wikipedia_mapper

    if 'data' not in request.get_json():
        return Response(status=400)

    input_data: list = request.get_json()['data']
    for icd10_code in input_data:
        icd11_code: str = icd_mapper.icd_10_to_icd_11(icd10_code)
        disease_name: str = icd_mapper.get_icd_10_name(icd10_code)
        eng_title, eng_url, pol_url = wikipedia_mapper.get_disease_wikipedia_data(icd10_code)
        db_controller.add_disease_entry(disease_name)
        id_disease: int = db_controller.get_disease_id_by_name(disease_name)
        db_controller.add_icd_codes(id_disease, icd_mapper.split_icd_10_code(icd10_code), icd11_code)
        db_controller.add_wiki_info(id_disease, 'eng', eng_title, eng_url)
        db_controller.add_wiki_info(id_disease, 'pol', '', pol_url)
    return Response(status=201)


def get_icd10(request, code: str):
    response_format: str = request.args.get('format')
    result: dict = db_controller.get_icd_10_info(code)

    if result == {}:
        return Response(status=404)

    if response_format == "json-pretty":
        return Response(response=json.dumps(result, indent=3), status=200, mimetype='application/json')
    else:
        return Response(response=json.dumps(result), status=200, mimetype='application/json')


def get_icd11(request, code: str):
    response_format: str = request.args.get('format')
    result: dict = db_controller.get_icd_11_info(code)
    if result == {}:
        return Response(status=404)

    if response_format == "json-pretty":
        return Response(response=json.dumps(result, indent=3), status=200, mimetype='application/json')
    else:
        return Response(response=json.dumps(result), status=200, mimetype='application/json')


def get_disease(request, id_disease: int):
    response_format: str = request.args.get('format')
    result: dict = db_controller.get_disease_info([id_disease])
    if result == {}:
        return Response(status=404)

    if response_format == "json-pretty":
        return Response(response=json.dumps(result, indent=3), status=200, mimetype='application/json')
    else:
        return Response(response=json.dumps(result), status=200, mimetype='application/json')


def add_additional_info(request) -> Response:
    data: dict = request.get_json()

    if not {'diseaseId', 'type', 'author', 'info'} <= request.get_json().keys():
        return Response(status=400)

    db_controller.add_additional_info(data['diseaseId'], data['type'], data['author'], data['info'])
    return Response(status=201)


def modify_additional_info(request) -> Response:
    data: dict = request.get_json()

    if not {'infoId', 'type', 'author', 'info'} <= request.get_json().keys():
        return Response(status=400)

    db_controller.modify_additional_info(data['infoId'], data['type'], data['author'], data['info'])
    return Response(status=201)


def delete_additional_info(id_disease: int) -> Response:
    db_controller.delete_additional_info(id_disease)
    return Response(status=200)