from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import math

class ReceiptPointsView(APIView):
    """API view for handling receipt-related operations and calculating points."""

    receipts = []

    def post(self, request):
        """
        Handles HTTP POST request to create a new receipt entry.

        Args:
            request (HttpRequest): The HTTP request object containing receipt data.

        Returns:
            Response: JSON response containing the receipt ID.
        """
        
        data = request.data
        receipt_id = len(self.receipts) + 1
        receipt_data = {
            "id": receipt_id,
            "retailer": data.get("retailer"),
            "purchaseDate": data.get("purchaseDate"),
            "purchaseTime": data.get("purchaseTime"),
            "items": data.get("items"),
            "total": data.get("total"),
        }
        self.receipts.append(receipt_data)
        return Response({"id": receipt_id}, status=status.HTTP_201_CREATED)

    def get(self, request, id):
        """
        Handles HTTP GET request to retrieve receipt points for a given receipt ID.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The ID of the receipt to retrieve points for.

        Returns:
            Response: JSON response containing the points for the receipt and status.
        """

        receipt = self.get_receipt_by_id(id)
        if receipt:
            points = self.calculate_points(receipt)
            return Response({"points": points}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Receipt not found"}, status=status.HTTP_404_NOT_FOUND)

    def get_receipt_by_id(self, receipt_id):
        """
        Retrieve a receipt by its ID.

        Args:
            receipt_id (int): The ID of the receipt to retrieve.

        Returns:
            dict or None: The receipt information if found, else None.
        """

        for receipt in self.receipts:
            if receipt["id"] == receipt_id:
                return receipt
        return None

    def calculate_points(self, receipt):
        """
        Calculate points based on the receipt information.

        Args:
            receipt (dict): The receipt information.

        Returns:
            int: The total points calculated based on the receipt.
        """

        total_points = 0

        # One point for every alphanumeric character in the retailer name
        for char in receipt["retailer"]:
            if char.isalnum():
                total_points += 1

        # 50 points if the total is a round dollar amount with no cents
        total_amount = float(receipt["total"])
        if total_amount.is_integer():
            total_points += 50
        
        # 25 points if the total is a multiple of 0.25
        if total_amount % 0.25 == 0:
            total_points += 25

        # 5 points for every two items on the receipt
        total_points += 5 * (len(receipt["items"]) // 2)  # 5 points for every two items

        # If the trimmed length of the item description is a multiple of 3, multiply 
        # the price by 0.2 and round up to the nearest integer to get the points
        for item in receipt["items"]:
            description_length = len(item["shortDescription"].strip())
            if description_length % 3 == 0:
                price = float(item["price"]) * 0.2
                total_points += math.ceil(price)

        # 6 points if the day in the purchase date is odd
        purchase_day = int(receipt["purchaseDate"].split("-")[2])
        if purchase_day % 2 != 0:
            total_points += 6

        # 10 points if the time of purchase is after 2:00pm and before 4:00pm
        purchase_hour = int(receipt["purchaseTime"].split(":")[0])
        purchase_minute = int(receipt["purchaseTime"].split(":")[1])
        if (purchase_hour >= 14 and purchase_minute != 0) and purchase_hour < 16:
            total_points += 10

        return total_points
