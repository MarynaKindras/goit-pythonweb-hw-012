import cloudinary
import cloudinary.uploader


class UploadFileService:
    """
    Сервіс для завантаження файлів на Cloudinary.

    Attributes:
        cloud_name (str): Назва хмарного сервісу
        api_key (str): Ключ API
        api_secret (str): Секретний ключ API
    """

    def __init__(self, cloud_name, api_key, api_secret):
        self.cloud_name = cloud_name
        self.api_key = api_key
        self.api_secret = api_secret
        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True,
        )

    @staticmethod
    def upload_file(file, username) -> str:
        """
        Завантажує файл на Cloudinary.

        Args:
            file: Файл для завантаження
            username (str): Ім'я користувача для унікального ідентифікатора

        Returns:
            str: URL завантаженого файлу
        """
        public_id = f"RestApp/{username}"
        r = cloudinary.uploader.upload(
            file.file, public_id=public_id, overwrite=True)
        src_url = cloudinary.CloudinaryImage(public_id).build_url(
            width=250, height=250, crop="fill", version=r.get("version")
        )
        return src_url
