import base64
import json
import boto3
import decimal


def lambda_handler(event, context):
    item = None
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("ServiceRequestEvents")
    decoded_record_data = [
        base64.b64decode(record["kinesis"]["data"]) for record in event["Records"]
    ]
    deserialized_data = [
        json.loads(decoded_record) for decoded_record in decoded_record_data
    ]

    with table.batch_writer() as batch_writer:
        for item in deserialized_data:
            casesummary = item["CaseSummary"]
            casestatus = item["CaseStatus"]
            casesource = item["CaseSource"]
            casecreateddate = item["CaseCreatedDate"]
            casecreateddttm = item["CaseCreateddttm"]
            casecloseddate = item["CaseClosedDate"]
            casecloseddttm = item["CaseCloseddttm"]
            firstcallresolution = item["FirstCallResolution"]
            customerzipcode = item["CustomerZipCode"]
            incidentaddress1 = item["IncidentAddress1"]
            incidentaddress2 = item["IncidentAddress2"]
            incidentintersection1 = item["IncidentIntersection1"]
            incidentintersection2 = item["IncidentIntersection2"]
            incidentzipcode = item["IncidentZipCode"]
            longitude = item["Longitude"]
            latitude = item["Latitude"]
            agency = item["Agency"]
            division = item["Division"]
            majorarea = item["MajorArea"]
            reqtype = item["Type"]
            topic = item["Topic"]
            councildistrict = item["CouncilDistrict"]
            policedistrict = item["PoliceDistrict"]
            neighborhood = item["Neighborhood"]

            batch_writer.put_item(
                Item={
                    "CaseSummary": casesummary,
                    "CaseStatus": casestatus,
                    "CaseSource": casesource,
                    "CaseCreatedDate": casecreateddate,
                    "CaseCreateddttm": casecreateddttm,
                    "CaseClosedDate": casecloseddate,
                    "CaseCloseddttm": casecloseddttm,
                    "FirstCallResolution": firstcallresolution,
                    "CustomerZipCode": customerzipcode,
                    "IncidentAddress1": incidentaddress1,
                    "IncidentAddress2": incidentaddress2,
                    "IncidentIntersection1": incidentintersection1,
                    "IncidentIntersection2": incidentintersection2,
                    "IncidentZipCode": incidentzipcode,
                    "Longitude": decimal.Decimal(longitude),
                    "Latitude": decimal.Decimal(latitude),
                    "Agency": agency,
                    "Division": division,
                    "MajorArea": majorarea,
                    "Type": reqtype,
                    "Topic": topic,
                    "CouncilDistrict": councildistrict,
                    "PoliceDistrict": policedistrict,
                    "Neighborhood": neighborhood,
                }
            )
