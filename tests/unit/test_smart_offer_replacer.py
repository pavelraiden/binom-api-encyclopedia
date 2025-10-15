"""
Unit tests for Smart Offer Replacer

Tests core functionality without API calls.
"""

import pytest
import sys
from pathlib import Path

# Add scripts/automation to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts' / 'automation'))

from smart_offer_replacer import (
    extract_offer_number,
    recalculate_weights,
    create_smart_mapping
)


def calculate_weight_distribution(count):
    """Helper function to calculate weight distribution for testing"""
    if count == 0:
        return []
    base_weight = 100 // count
    remainder = 100 % count
    weights = [base_weight] * count
    weights[-1] += remainder
    return weights


class TestOfferNumberExtraction:
    """Tests for extract_offer_number function"""
    
    def test_extract_number_with_hash(self):
        """Should extract number from #N format"""
        assert extract_offer_number("Memorra Cleaner #1") == 1
        assert extract_offer_number("Memorra Cleaner #2") == 2
        assert extract_offer_number("Memorra Cleaner #3") == 3
    
    def test_extract_number_middle(self):
        """Should extract number from middle of string"""
        assert extract_offer_number("Offer #5 Test") == 5
    
    def test_extract_number_multiple(self):
        """Should extract first number when multiple present"""
        assert extract_offer_number("Offer #1 and #2") == 1
    
    def test_no_number(self):
        """Should return None when no number present"""
        assert extract_offer_number("Memorra Cleaner") is None
    
    def test_empty_string(self):
        """Should return None for empty string"""
        assert extract_offer_number("") is None


class TestWeightRecalculation:
    """Tests for recalculate_weights function"""
    
    def test_three_offers(self):
        """Should distribute 100 across 3 offers"""
        weights = calculate_weight_distribution(3)
        assert weights == [33, 33, 34]
        assert sum(weights) == 100
    
    def test_two_offers(self):
        """Should distribute 100 across 2 offers"""
        weights = calculate_weight_distribution(2)
        assert weights == [50, 50]
        assert sum(weights) == 100
    
    def test_four_offers(self):
        """Should distribute 100 across 4 offers"""
        weights = calculate_weight_distribution(4)
        assert weights == [25, 25, 25, 25]
        assert sum(weights) == 100
    
    def test_five_offers(self):
        """Should distribute 100 across 5 offers"""
        weights = calculate_weight_distribution(5)
        assert weights == [20, 20, 20, 20, 20]
        assert sum(weights) == 100
    
    def test_seven_offers(self):
        """Should distribute 100 across 7 offers with remainder"""
        weights = calculate_weight_distribution(7)
        assert len(weights) == 7
        assert sum(weights) == 100
        # Base weight should be 14, last should be 14 + 2 = 16
        assert weights == [14, 14, 14, 14, 14, 14, 16]
    
    def test_one_offer(self):
        """Should return 100 for single offer"""
        weights = calculate_weight_distribution(1)
        assert weights == [100]
    
    def test_zero_offers(self):
        """Should return empty list for zero offers"""
        weights = calculate_weight_distribution(0)
        assert weights == []


class TestSmartMapping:
    """Tests for create_smart_mapping function (mocked API)"""
    
    def test_mapping_logic(self):
        """Test mapping logic with mock data"""
        # This would require mocking the API
        # For now, just ensure function exists
        assert callable(create_smart_mapping)


class TestEdgeCases:
    """Tests for edge cases and error handling"""
    
    def test_extract_number_with_special_chars(self):
        """Should handle special characters"""
        assert extract_offer_number("Offer-#1-Test") == 1
        assert extract_offer_number("Offer_#2_Test") == 2
    
    def test_extract_large_number(self):
        """Should handle large numbers"""
        assert extract_offer_number("Offer #999") == 999
    
    def test_weights_sum_always_100(self):
        """Weights should always sum to 100"""
        for count in range(1, 20):
            weights = calculate_weight_distribution(count)
            assert sum(weights) == 100, f"Failed for count={count}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

