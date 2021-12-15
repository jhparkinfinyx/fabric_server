from celery import Celery

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
app = Celery('async_tasks', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)



# 이미지 업로드 -> (모델처리)
# 모델처리 : celery 처리

@celery.task(bind=True)
def image_get_process(self, mail_list):
	with app.app_context():
		total = len(mail_list) - 1
		for idx, mail in enumerate(mail_list):
			# mail_send #
			time.sleep(2.0/random.randint(1,4))
			self.update_state(state='PROGRESS', meta={'current': idx, 'total': total})
		return {'current': idx, 'total': total}