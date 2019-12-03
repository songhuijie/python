import logging

def RecordLog(msg):
    callfile = '/var/www/html/xvideo_csv/log/test.log'
    logging.basicConfig(filename=callfile, filemode="a", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)
    logging.info(msg)

    return True

def main():

    RecordLog('test')


if __name__ == '__main__':
    main()