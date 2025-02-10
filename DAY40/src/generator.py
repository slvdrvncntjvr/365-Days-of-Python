import qrcode
from typing import Optional
from pathlib import Path

class QRCodeGenerator:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

    def generate(
        self, 
        data: str, 
        output_path: Optional[str] = None
    ) -> Optional[str]:
       
        try:
            self.qr.clear()
            self.qr.add_data(data)
            self.qr.make(fit=True)

            
            qr_image = self.qr.make_image(fill_color="black", back_color="white")

            if output_path:
                
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                
                
                qr_image.save(output_path)
                return output_path
                
            return None
            
        except Exception as e:
            raise Exception(f"Error generating QR code: {str(e)}")