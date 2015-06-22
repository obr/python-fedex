"""
Upload Document Service Module
=======================
This package contains the upload document methods defined by Fedex's
UploadDocumentService WSDL file. Each is encapsulated in a class for easy access.
For more details on each, refer to the respective class's documentation.
"""
import base64
import os

from .. base_service import FedexBaseService, FedexError


class FedexInvalidUploadDocumentRequest(FedexError):
    """
    Exception: Sent when a bad upload document request is done.
    """

    pass


class FedexUploadDocumentRequest(FedexBaseService):
    """
    This class allows you to upload documents for later referral.
    """

    def __init__(self, config_obj, *args, **kwargs):
        """
        Sends a shipment tracking request. The optional keyword args
        detailed on L{FedexBaseService} apply here as well.
        
        @type config_obj: L{FedexConfig}
        @param config_obj: A valid FedexConfig object.
        
        @type tracking_number_unique_id: str
        @param tracking_number_unique_id: Used to distinguish duplicate FedEx tracking numbers.
        """

        self._config_obj = config_obj
        
        # Holds version info for the VersionId SOAP object.
        self._version_info = {
            'service_id': 'cdus',
            'major': '7',
            'intermediate': '0',
            'minor': '0'
        }

        self.DestinationCountryCode = kwargs.pop('destination_country_code', None)
        """@ivar: Destination country code."""

        self.OriginCountryCode = kwargs.pop('origin_country_code', None)
        """@ivar: Origin country code."""

        # Call the parent FedexBaseService class for basic setup work.
        super(FedexUploadDocumentRequest, self).__init__(
            self._config_obj, 'UploadDocumentService_v7.wsdl', *args, **kwargs)

    def _prepare_wsdl_objects(self):
        """
        This is the data that will be used to upload documents. Create
        the data structure and get it ready for the WSDL request.
        """
        self.Documents = []
        self.Usage = "ELECTRONIC_TRADE_DOCUMENTS"

    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.
        
        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(), WHICH RESIDES
            ON FedexBaseService AND IS INHERITED.
        """

        client = self.client
        # Fire off the query.
        return client.service.uploadDocuments(
            WebAuthenticationDetail=self.WebAuthenticationDetail,
            ClientDetail=self.ClientDetail,
            TransactionDetail=self.TransactionDetail,
            Version=self.VersionId,
            OriginCountryCode=self.OriginCountryCode,
            DestinationCountryCode=self.DestinationCountryCode,
            Documents=self.Documents)

    def add_file_document(self, file_path, document_type="OTHER", file_name=None, reference_message=None):
        assert document_type in (
            "CERTIFICATE_OF_ORIGIN",
            "COMMERCIAL_INVOICE",
            "ETD_LABEL",
            "NAFTA_CERTIFICATE_OF_ORIGIN",
            "OTHER",
            "PRO_FORMA_INVOICE",), "Unsupported document type {}.".format(document_type)

        with open(file_path, "rb") as document_file:
            encoded_document_data = base64.b64encode(document_file.read())
            document = self.create_wsdl_object_of_type("UploadDocumentDetail")

            document.DocumentType = document_type
            document.FileName = file_name or os.path.basename(file_path)
            if reference_message:
                document.CustomerReference = reference_message
            document.DocumentContent = encoded_document_data
            self.Documents.append(document)
