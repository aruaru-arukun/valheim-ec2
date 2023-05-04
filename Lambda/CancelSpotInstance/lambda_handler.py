import logging
import boto3
from botocore.client import BaseClient


def handler(event: dict, context: dict) -> None:
    logging.info(event)
    logging.info(context)

    # インスタンスIDで終了済みのスポットインスタンスを取得する
    client: BaseClient = boto3.client("ec2")
    response: dict = client.describe_instances(
        Filters=[
            {"Name": "instance-lifecycle", "Values": ["spot"]},
        ],
        InstanceIds=[event["detail"]["instance-id"]],
    )

    # 対象が存在しない場合は処理終了
    if not response["Reservations"] and response["Reservations"][0]["Instances"]:
        logging.info("not spot instance")
        return

    # spotIDを取得
    spot_request_id: str = response["Reservations"][0]["Instances"][0][
        "SpotInstanceRequestId"
    ]

    # スポットリクエストをキャンセル
    client.cancel_spot_instance_requests(SpotInstanceRequestIds=[spot_request_id])
    logging.info("Your spot request has been canceled->{spot_request_id}")
