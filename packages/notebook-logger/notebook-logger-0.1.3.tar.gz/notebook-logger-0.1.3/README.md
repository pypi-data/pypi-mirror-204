# notebook-logger
logging for jupyternotebook  
  
  
## Version
    0.1.2

## Installation
    pip install notebook-logger

## How to
    from notebook_logger import SimpleLogger

    logger = SimpleLogger('test.log', is_print=False)
    logger.log('Only log file')
    logger.log('Both console and file', is_print=True)
    