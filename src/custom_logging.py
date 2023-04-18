import logging

FORMAT = '%(levelname)s %(asctime)s -> %(module)s:%(lineno)d %(message)s'
logging.basicConfig(
	level=logging.INFO,
	handlers=[
		logging.FileHandler('app.log'),
		logging.StreamHandler()
	],
	format=FORMAT,
	datefmt='%d-%m-%Y %I:%M %p'
)
logger = logging.getLogger()

if __name__ == '__main__':
	logger.info('Ocurrio un error desde logging info')
	logger.warning('Ocurrio un error desde logging warning')
	logger.error('Ocurrio un error desde logging error')
	logger.critical('Ocurrio un error desde logging critical')
