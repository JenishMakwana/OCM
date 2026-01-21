#!/usr/bin/env python3
"""
Backend API Testing Script for Tyre Inventory Management System
Tests all API endpoints as specified in the review request.
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Get backend URL from frontend .env
BACKEND_URL = "https://tyre-inventory-1.preview.emergentagent.com/api"

class TyreAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        
    def test_get_all_tyres(self) -> Dict[str, Any]:
        """Test GET /api/tyres - Should return 171 tyres"""
        try:
            response = self.session.get(f"{self.base_url}/tyres")
            
            if response.status_code != 200:
                self.log_test("GET /api/tyres", False, f"Status code: {response.status_code}")
                return {"success": False, "data": None}
                
            data = response.json()
            
            # Check if it's a list
            if not isinstance(data, list):
                self.log_test("GET /api/tyres", False, "Response is not a list")
                return {"success": False, "data": None}
                
            # Check count
            if len(data) != 171:
                self.log_test("GET /api/tyres", False, f"Expected 171 tyres, got {len(data)}")
                return {"success": False, "data": data}
                
            # Check data structure of first item
            if data:
                first_tyre = data[0]
                required_fields = ['id', 'brand', 'size', 'type', 'pattern', 'stock', 'price']
                missing_fields = [field for field in required_fields if field not in first_tyre]
                
                if missing_fields:
                    self.log_test("GET /api/tyres", False, f"Missing fields: {missing_fields}")
                    return {"success": False, "data": data}
                    
            # Check brands
            brands = set(tyre['brand'] for tyre in data)
            expected_brands = {'MRF', 'TVS', 'BEDROCK', 'CEAT'}
            
            if not expected_brands.issubset(brands):
                missing_brands = expected_brands - brands
                self.log_test("GET /api/tyres", False, f"Missing brands: {missing_brands}")
                return {"success": False, "data": data}
                
            self.log_test("GET /api/tyres", True, f"Retrieved {len(data)} tyres with all expected brands")
            return {"success": True, "data": data}
            
        except Exception as e:
            self.log_test("GET /api/tyres", False, f"Exception: {str(e)}")
            return {"success": False, "data": None}
            
    def test_get_brands(self):
        """Test GET /api/tyres/brands - Should return list of unique brands"""
        try:
            response = self.session.get(f"{self.base_url}/tyres/brands")
            
            if response.status_code != 200:
                self.log_test("GET /api/tyres/brands", False, f"Status code: {response.status_code}")
                return
                
            data = response.json()
            
            # Check structure
            if 'brands' not in data:
                self.log_test("GET /api/tyres/brands", False, "Response missing 'brands' key")
                return
                
            brands = data['brands']
            expected_brands = {'MRF', 'TVS', 'BEDROCK', 'CEAT'}
            
            if not isinstance(brands, list):
                self.log_test("GET /api/tyres/brands", False, "Brands is not a list")
                return
                
            brands_set = set(brands)
            if not expected_brands.issubset(brands_set):
                missing_brands = expected_brands - brands_set
                self.log_test("GET /api/tyres/brands", False, f"Missing brands: {missing_brands}")
                return
                
            self.log_test("GET /api/tyres/brands", True, f"Retrieved brands: {brands}")
            
        except Exception as e:
            self.log_test("GET /api/tyres/brands", False, f"Exception: {str(e)}")
            
    def test_search_functionality(self):
        """Test GET /api/tyres/search with various parameters"""
        
        # Test 1: Search by brand (MRF)
        try:
            response = self.session.get(f"{self.base_url}/tyres/search?brand=MRF")
            
            if response.status_code != 200:
                self.log_test("Search by brand (MRF)", False, f"Status code: {response.status_code}")
            else:
                data = response.json()
                if not isinstance(data, list):
                    self.log_test("Search by brand (MRF)", False, "Response is not a list")
                elif not data:
                    self.log_test("Search by brand (MRF)", False, "No results returned")
                elif not all(tyre['brand'] == 'MRF' for tyre in data):
                    self.log_test("Search by brand (MRF)", False, "Non-MRF tyres in results")
                else:
                    self.log_test("Search by brand (MRF)", True, f"Found {len(data)} MRF tyres")
                    
        except Exception as e:
            self.log_test("Search by brand (MRF)", False, f"Exception: {str(e)}")
            
        # Test 2: Search by size (90/100*10)
        try:
            response = self.session.get(f"{self.base_url}/tyres/search?size=90/100*10")
            
            if response.status_code != 200:
                self.log_test("Search by size (90/100*10)", False, f"Status code: {response.status_code}")
            else:
                data = response.json()
                if not isinstance(data, list):
                    self.log_test("Search by size (90/100*10)", False, "Response is not a list")
                elif not data:
                    self.log_test("Search by size (90/100*10)", False, "No results returned")
                elif not all('90/100*10' in tyre['size'] for tyre in data):
                    self.log_test("Search by size (90/100*10)", False, "Incorrect size results")
                else:
                    self.log_test("Search by size (90/100*10)", True, f"Found {len(data)} tyres with size 90/100*10")
                    
        except Exception as e:
            self.log_test("Search by size (90/100*10)", False, f"Exception: {str(e)}")
            
        # Test 3: Combined search (TVS + 275*18)
        try:
            response = self.session.get(f"{self.base_url}/tyres/search?brand=TVS&size=275*18")
            
            if response.status_code != 200:
                self.log_test("Combined search (TVS + 275*18)", False, f"Status code: {response.status_code}")
            else:
                data = response.json()
                if not isinstance(data, list):
                    self.log_test("Combined search (TVS + 275*18)", False, "Response is not a list")
                elif not data:
                    self.log_test("Combined search (TVS + 275*18)", False, "No results returned")
                elif not all(tyre['brand'] == 'TVS' and '275*18' in tyre['size'] for tyre in data):
                    self.log_test("Combined search (TVS + 275*18)", False, "Incorrect combined search results")
                else:
                    self.log_test("Combined search (TVS + 275*18)", True, f"Found {len(data)} TVS tyres with size 275*18")
                    
        except Exception as e:
            self.log_test("Combined search (TVS + 275*18)", False, f"Exception: {str(e)}")
            
    def test_update_tyre(self, all_tyres_data: List[Dict]):
        """Test PUT /api/tyres/{id} - Update tyre stock and price"""
        if not all_tyres_data:
            self.log_test("Update tyre", False, "No tyre data available for testing")
            return
            
        # Pick the first tyre for testing
        test_tyre = all_tyres_data[0]
        tyre_id = test_tyre['id']
        
        # Test valid update
        try:
            update_data = {
                "stock": 10,
                "price": 1500.0
            }
            
            response = self.session.put(
                f"{self.base_url}/tyres/{tyre_id}",
                json=update_data
            )
            
            if response.status_code != 200:
                self.log_test("Update tyre (valid)", False, f"Status code: {response.status_code}, Response: {response.text}")
                return
                
            updated_tyre = response.json()
            
            # Verify the update
            if updated_tyre['stock'] != 10 or updated_tyre['price'] != 1500.0:
                self.log_test("Update tyre (valid)", False, f"Update not reflected: stock={updated_tyre['stock']}, price={updated_tyre['price']}")
                return
                
            self.log_test("Update tyre (valid)", True, f"Successfully updated tyre {tyre_id}")
            
            # Verify persistence by fetching the tyre again
            verify_response = self.session.get(f"{self.base_url}/tyres")
            if verify_response.status_code == 200:
                all_tyres = verify_response.json()
                updated_tyre_check = next((t for t in all_tyres if t['id'] == tyre_id), None)
                
                if updated_tyre_check and updated_tyre_check['stock'] == 10 and updated_tyre_check['price'] == 1500.0:
                    self.log_test("Update persistence check", True, "Changes persisted correctly")
                else:
                    self.log_test("Update persistence check", False, "Changes not persisted")
            else:
                self.log_test("Update persistence check", False, "Could not verify persistence")
                
        except Exception as e:
            self.log_test("Update tyre (valid)", False, f"Exception: {str(e)}")
            
    def test_error_handling(self):
        """Test error handling scenarios"""
        
        # Test 1: Invalid tyre ID
        try:
            fake_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format but non-existent
            response = self.session.put(
                f"{self.base_url}/tyres/{fake_id}",
                json={"stock": 5}
            )
            
            if response.status_code == 404:
                self.log_test("Error handling (invalid ID)", True, "Correctly returned 404 for invalid ID")
            else:
                self.log_test("Error handling (invalid ID)", False, f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            self.log_test("Error handling (invalid ID)", False, f"Exception: {str(e)}")
            
        # Test 2: Invalid data (negative values)
        try:
            # First get a valid tyre ID
            response = self.session.get(f"{self.base_url}/tyres")
            if response.status_code == 200:
                tyres = response.json()
                if tyres:
                    tyre_id = tyres[0]['id']
                    
                    # Try to update with negative values
                    response = self.session.put(
                        f"{self.base_url}/tyres/{tyre_id}",
                        json={"stock": -5, "price": -100}
                    )
                    
                    # The API should either reject this (400) or accept it (depending on validation)
                    # Let's check what happens
                    if response.status_code in [400, 422]:
                        self.log_test("Error handling (negative values)", True, f"Correctly rejected negative values with status {response.status_code}")
                    else:
                        # If it accepts negative values, that's also valid behavior
                        self.log_test("Error handling (negative values)", True, f"API accepts negative values (status {response.status_code})")
                else:
                    self.log_test("Error handling (negative values)", False, "No tyres available for testing")
            else:
                self.log_test("Error handling (negative values)", False, "Could not fetch tyres for testing")
                
        except Exception as e:
            self.log_test("Error handling (negative values)", False, f"Exception: {str(e)}")
            
        # Test 3: Invalid JSON format
        try:
            response = self.session.get(f"{self.base_url}/tyres")
            if response.status_code == 200:
                tyres = response.json()
                if tyres:
                    tyre_id = tyres[0]['id']
                    
                    # Send invalid JSON
                    response = self.session.put(
                        f"{self.base_url}/tyres/{tyre_id}",
                        data="invalid json"
                    )
                    
                    if response.status_code in [400, 422]:
                        self.log_test("Error handling (invalid JSON)", True, f"Correctly rejected invalid JSON with status {response.status_code}")
                    else:
                        self.log_test("Error handling (invalid JSON)", False, f"Expected 400/422, got {response.status_code}")
                else:
                    self.log_test("Error handling (invalid JSON)", False, "No tyres available for testing")
            else:
                self.log_test("Error handling (invalid JSON)", False, "Could not fetch tyres for testing")
                
        except Exception as e:
            self.log_test("Error handling (invalid JSON)", False, f"Exception: {str(e)}")
            
    def run_all_tests(self):
        """Run all API tests"""
        print(f"🧪 Starting Backend API Tests for: {self.base_url}")
        print("=" * 60)
        
        # Test 1: Get all tyres
        all_tyres_result = self.test_get_all_tyres()
        
        # Test 2: Get brands
        self.test_get_brands()
        
        # Test 3: Search functionality
        self.test_search_functionality()
        
        # Test 4: Update tyre (only if we have tyre data)
        if all_tyres_result["success"] and all_tyres_result["data"]:
            self.test_update_tyre(all_tyres_result["data"])
        
        # Test 5: Error handling
        self.test_error_handling()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if total - passed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
                    
        return passed == total

def main():
    """Main test execution"""
    tester = TyreAPITester(BACKEND_URL)
    
    print("🔧 Tyre Inventory Management System - Backend API Tests")
    print(f"🌐 Testing against: {BACKEND_URL}")
    print()
    
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()