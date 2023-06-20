import json
import unittest
from app import app
from unittest.mock import patch

@patch('app.pointsDict', {'7fb1377b-b223-49d9-a31a-5a02701dd310' : 32}) 
class ApiTests(unittest.TestCase) :

    def test_process_invalid_receipt(self) :
        # invalid because missing closing brace
        sample_receipt = '''{
            "retailer": "Walgreens",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "08:13",
            "total": "2.65",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.40"}
            ]
        '''
        response = response=app.test_client().post('/receipts/process', 
                       data=sample_receipt,
                       content_type='application/json')
        assert response.status_code == 400

    def test_process_valid_receipt(self) :
        sample_receipt = {
            "retailer": "Walgreens",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "08:13",
            "total": "2.65",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.40"}
            ]
        }
        response=app.test_client().post('/receipts/process', 
                       data=json.dumps(sample_receipt),
                       content_type='application/json')
        
        assert response.content_type == 'application/json'
        assert response.status_code == 200
        assert "id" in json.loads(response.data)

    def test_get_points_invalid_id(self) :
        response=app.test_client().get('/receipts/someid/points')
        assert response.status_code == 404

    def test_get_points_valid_id(self) :
        response=app.test_client().get('/receipts/7fb1377b-b223-49d9-a31a-5a02701dd310/points')
        assert response.status_code == 200
        assert json.loads(response.data)['points'] == 32


if __name__ == "__main__":
    unittest.main()
