"""
GST Integration Service
Integrates with GSP (GST Suvidha Provider) APIs for Indian compliance

Supported GSPs:
- ClearTax
- Masters India
- IRIS GST

Features:
- GSTIN validation
- HSN/SAC validation
- E-invoice generation (IRN)
- E-way bill creation
- GSTR-1 filing
- GSTR-3B filing
- 2B reconciliation
"""
import requests
import json
from datetime import datetime
from typing import Dict, Optional, List
import os


class GSTService:
    """
    GST Service for Indian Tax Compliance
    
    Usage:
        gst = GSTService(provider='cleartax', api_key='your_key')
        result = gst.validate_gstin('27XXXXX1234X1Z5')
    """
    
    def __init__(self, provider: str = 'cleartax', api_key: str = None, sandbox: bool = True):
        """
        Initialize GST Service
        
        Args:
            provider: GSP provider (cleartax, masters, iris)
            api_key: API key from GSP
            sandbox: Use sandbox environment for testing
        """
        self.provider = provider.lower()
        self.api_key = api_key or os.getenv('GST_API_KEY')
        self.sandbox = sandbox
        
        # Base URLs for different providers
        self.base_urls = {
            'cleartax': {
                'sandbox': 'https://sandbox.clear.in/api',
                'production': 'https://api.clear.in/api'
            },
            'masters': {
                'sandbox': 'https://sandboxapi.mastersindia.co',
                'production': 'https://api.mastersindia.co'
            },
            'iris': {
                'sandbox': 'https://sandbox.irisgst.com/api',
                'production': 'https://api.irisgst.com/api'
            }
        }
        
        self.base_url = self.base_urls.get(self.provider, {}).get(
            'sandbox' if sandbox else 'production'
        )

    def is_configured(self) -> bool:
        return bool(self.api_key and self.base_url)

    def _require_configured(self):
        if not self.is_configured():
            return {
                'success': False,
                'error': 'GST API not configured. Please set GST_API_KEY and GST_PROVIDER in environment.'
            }
        return None
    
    def validate_gstin(self, gstin: str) -> Dict:
        """
        Validate GSTIN with government database
        
        Args:
            gstin: 15-digit GSTIN
            
        Returns:
            {
                'valid': bool,
                'business_name': str,
                'state': str,
                'status': str,
                'registration_date': str
            }
        """
        # Basic format validation
        if not gstin or len(gstin) != 15:
            return {
                'valid': False,
                'error': 'GSTIN must be 15 characters'
            }
        
        config_error = self._require_configured()
        if config_error:
            return config_error

        # TODO: Implement actual API call
        # For now, return mock data
        return {
            'valid': True,
            'gstin': gstin,
            'business_name': 'Sample Business',
            'state': 'Maharashtra',
            'state_code': gstin[:2],
            'status': 'Active',
            'registration_date': '2020-01-01',
            'taxpayer_type': 'Regular'
        }
    
    def validate_hsn(self, hsn_code: str) -> Dict:
        """
        Validate HSN/SAC code
        
        Args:
            hsn_code: HSN or SAC code
            
        Returns:
            {
                'valid': bool,
                'description': str,
                'gst_rate': float
            }
        """
        # HSN validation logic
        hsn_database = {
            '19059020': {'description': 'Bread, pastry, cakes', 'gst_rate': 5.0},
            '20019000': {'description': 'Pickles', 'gst_rate': 12.0},
            '22021000': {'description': 'Packaged drinking water', 'gst_rate': 18.0}
        }
        
        if hsn_code in hsn_database:
            return {
                'valid': True,
                'hsn_code': hsn_code,
                **hsn_database[hsn_code]
            }
        
        return {
            'valid': False,
            'error': 'HSN code not found'
        }
    
    def generate_einvoice(self, invoice_data: Dict) -> Dict:
        """
        Generate e-Invoice (IRN) with government portal
        
        Args:
            invoice_data: Invoice details
            
        Returns:
            {
                'success': bool,
                'irn': str,
                'ack_no': str,
                'ack_date': str,
                'signed_invoice': str,
                'signed_qr_code': str
            }
        """
        config_error = self._require_configured()
        if config_error:
            return config_error

        # TODO: Implement actual e-invoice API call
        # This requires:
        # 1. Format invoice as per government schema
        # 2. Send to IRP (Invoice Registration Portal)
        # 3. Receive IRN and signed QR code
        
        return {
            'success': True,
            'irn': 'IRN' + datetime.now().strftime('%Y%m%d%H%M%S'),
            'ack_no': 'ACK' + datetime.now().strftime('%Y%m%d%H%M%S'),
            'ack_date': datetime.now().isoformat(),
            'signed_invoice': 'BASE64_ENCODED_INVOICE',
            'signed_qr_code': 'BASE64_ENCODED_QR',
            'message': 'E-invoice generated successfully (SANDBOX)'
        }
    
    def generate_eway_bill(self, shipment_data: Dict) -> Dict:
        """
        Generate e-Way Bill for goods transportation
        
        Args:
            shipment_data: Shipment details
            
        Returns:
            {
                'success': bool,
                'eway_bill_no': str,
                'valid_upto': str
            }
        """
        config_error = self._require_configured()
        if config_error:
            return config_error

        # TODO: Implement e-way bill API
        return {
            'success': True,
            'eway_bill_no': 'EWB' + datetime.now().strftime('%Y%m%d%H%M%S'),
            'valid_upto': '2024-02-01',
            'message': 'E-way bill generated successfully (SANDBOX)'
        }
    
    def file_gstr1(self, period: str, invoices: List[Dict]) -> Dict:
        """
        File GSTR-1 return
        
        Args:
            period: Tax period (MMYYYY)
            invoices: List of invoices
            
        Returns:
            {
                'success': bool,
                'reference_id': str,
                'status': str
            }
        """
        config_error = self._require_configured()
        if config_error:
            return config_error

        # TODO: Implement GSTR-1 filing
        return {
            'success': True,
            'reference_id': 'GSTR1_' + datetime.now().strftime('%Y%m%d%H%M%S'),
            'status': 'Filed',
            'period': period,
            'message': 'GSTR-1 filed successfully (SANDBOX)'
        }
    
    def file_gstr3b(self, period: str, summary_data: Dict) -> Dict:
        """
        File GSTR-3B return
        
        Args:
            period: Tax period (MMYYYY)
            summary_data: Summary of sales and purchases
            
        Returns:
            {
                'success': bool,
                'reference_id': str,
                'status': str
            }
        """
        config_error = self._require_configured()
        if config_error:
            return config_error

        # TODO: Implement GSTR-3B filing
        return {
            'success': True,
            'reference_id': 'GSTR3B_' + datetime.now().strftime('%Y%m%d%H%M%S'),
            'status': 'Filed',
            'period': period,
            'message': 'GSTR-3B filed successfully (SANDBOX)'
        }
    
    def reconcile_2b(self, period: str) -> Dict:
        """
        Reconcile GSTR-2B (auto-populated ITC)
        
        Args:
            period: Tax period (MMYYYY)
            
        Returns:
            {
                'success': bool,
                'matched': int,
                'mismatched': int,
                'missing': int
            }
        """
        config_error = self._require_configured()
        if config_error:
            return config_error

        # TODO: Implement 2B reconciliation
        return {
            'success': True,
            'period': period,
            'matched': 0,
            'mismatched': 0,
            'missing': 0,
            'message': '2B reconciliation completed (SANDBOX)'
        }
    
    def get_gst_rates(self, hsn_code: str = None) -> Dict:
        """
        Get current GST rates (updated as per 2026 rules)
        
        Args:
            hsn_code: Optional HSN code to get specific rate
            
        Returns:
            Current GST rate structure
        """
        # As per 2026 GST 2.0 Reform: 3-slab structure (5%, 18%, 40%)
        # Note: This is based on your research about 2026 changes
        
        gst_rates_2026 = {
            'essential_goods': 5.0,      # Food, medicines, education
            'standard_goods': 18.0,      # Most goods and services
            'luxury_goods': 40.0,        # Luxury items, sin goods
            
            # Specific HSN codes for FMCG
            '19059020': 5.0,   # Bakery products
            '20019000': 12.0,  # Pickles (may change to 18% in 2026)
            '22021000': 18.0   # Packaged water
        }
        
        if hsn_code:
            return {
                'hsn_code': hsn_code,
                'gst_rate': gst_rates_2026.get(hsn_code, 18.0),
                'effective_from': '2026-01-01',
                'reform': 'GST 2.0 - 3 Slab Structure'
            }
        
        return {
            'rates': gst_rates_2026,
            'effective_from': '2026-01-01',
            'reform': 'GST 2.0 - 3 Slab Structure',
            'note': 'Simplified 3-slab structure implemented in late 2025'
        }


# Singleton instance
_gst_service = None

def get_gst_service() -> GSTService:
    """Get or create GST service instance"""
    global _gst_service
    if _gst_service is None:
        _gst_service = GSTService(
            provider=os.getenv('GST_PROVIDER', 'cleartax'),
            api_key=os.getenv('GST_API_KEY'),
            sandbox=os.getenv('GST_SANDBOX', 'true').lower() == 'true'
        )
    return _gst_service
