from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    
    # Security Scan Results
    has_dep = models.BooleanField(default=False, help_text="Data Execution Prevention")
    has_aslr = models.BooleanField(default=False, help_text="Address Space Layout Randomization")
    is_safe = models.BooleanField(default=True)
    
    sha256_hash = models.CharField(max_length=64, blank=True, help_text="SHA-256 Hash of the file")

    def __str__(self):
        return self.file_name