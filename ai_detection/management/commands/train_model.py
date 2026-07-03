from django.core.management.base import BaseCommand
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class Command(BaseCommand):
    help = 'Train the LoanGuard AI fraud detection model'

    def handle(self, *args, **options):
        self.stdout.write('Training LoanGuard AI model...')
        from ai_detection.train_model import train_and_save
        acc = train_and_save()
        if acc:
            self.stdout.write(self.style.SUCCESS(f'Model trained! Accuracy: {acc*100:.1f}%'))
