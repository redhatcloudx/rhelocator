from typing import Optional

from flasgger import swag_from
from flask import Blueprint
from flask import request


def aws_blueprint(data: list[dict[str, str]]) -> Blueprint:
    """Creates and returns a Flask blueprint based that serves the provided
    image data.

    Args:
        data: Formatted image data dict.

    Returns:
        Flask blueprint serving the provided data.
    """
    aws_endpoint = Blueprint("aws_api", __name__)

    @aws_endpoint.route("/aws", methods=["GET"])
    @swag_from("../schema/aws.yml")
    def endpoint() -> list[dict[str, str]]:
        """Cloud Image Locator AWS Endpoint Provides RHEL image data for AWS
        Cloud."""

        query: dict[str, str] = {}
        name: Optional[str] = request.args.get("name")
        arch: Optional[str] = request.args.get("arch")
        image_id: Optional[str] = request.args.get("imageId")
        date: Optional[str] = request.args.get("date")
        version: Optional[str] = request.args.get("version")
        virt: Optional[str] = request.args.get("virt")
        region: Optional[str] = request.args.get("region")

        if name:
            query.update({"name": name})
        if arch:
            query.update({"arch": arch})
        if image_id:
            query.update({"imageId": image_id})
        if date:
            query.update({"date": date})
        if version:
            query.update({"version": version})
        if virt:
            query.update({"virt": virt})
        if region:
            query.update({"region": region})

        if len(query) == 0:
            return data

        response: list[dict[str, str]] = []
        for image in data:
            add_image = True
            for key, value in query.items():
                if value not in image[key]:
                    add_image = False
                    break
            if add_image:
                response.append(image)
        return response

    return aws_endpoint
