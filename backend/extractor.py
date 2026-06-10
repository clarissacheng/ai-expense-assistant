import os
import base64
import json
import sys

from openai import OpenAI
from dotenv import load_dotenv
from backend.db import load_corrections

load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)

def extract_receipt_data(image_bytes):
    corrections = load_corrections()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    prompt = f"""
        You are extracting structured data from a receipt.

        Use these corrections:
        {json.dumps(corrections, indent=2)}

        First determine whether the image is actually a receipt.

        If the image is NOT a receipt
        (for example: a selfie, landscape, pet photo, screenshot,
        document, meme, blank image, random object, etc.)

        Return ONLY:

        {{
        "not_receipt": true
        }}

        Otherwise return ONLY valid JSON matching this schema:

        {{
        "not_receipt": false,
        "store_name": "string",
        "date": "string",
        "items": [
            {{
            "name": "string",
            "unit_price": 0,
            "quantity": 0,
            "total_price": 0,
            "category": "string (AUTOMATICALLY ASSIGN BEST FIT CATEGORY)"
            }}
        ],
        "total": 0
        }}

        Rules:
        - Normalize store names using corrections
        - Normalize item categories using corrections
        - You MUST assign a category for every item
        - Categories should be short and consistent
        - Prefer reuse of categories when items are similar across receipts
        - Infer category from item name if not obvious
        - Do not hallucinate fields
        - If uncertain whether the image is a receipt, return not_receipt=true
        - Return ONLY valid JSON
        """

    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    ]
                }
            ]
        )

        text = response.output[0].content[0].text

        def parse_json(text):
            try:
                return json.loads(text)
            except:
                start = text.find("{")
                end = text.rfind("}") + 1
                if start != -1 and end != -1:
                    try:
                        return json.loads(text[start:end])
                    except:
                        pass
                return {"error": "Could not parse JSON", "raw_output": text}

        data = parse_json(text)

        # safer dedup
        if "items" in data:
            seen = {}
            for item in data["items"]:
                name = item.get("name", "").lower().strip()
                price = float(item.get("unit_price", item.get("price", 0)) or 0)

                if name in seen:
                    seen[name]["quantity"] += 1
                    seen[name]["total_price"] += price
                else:
                    seen[name] = {
                        "name": item.get("name"),
                        "unit_price": price,
                        "quantity": 1,
                        "total_price": price,
                        "category": item.get("category", "")
                    }

            data["items"] = list(seen.values())

        return data

    except Exception as e:
        return {
            "error": str(e)
        }


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        print(extract_receipt_data(f.read()))