from logger import logger


def query_chain(chain, user_input: str):
    try:
        logger.debug(f"Running chain for input: {user_input}")
        result = chain({"query": user_input})
        response = {
            "response": result["result"],
            "source_documents": result["source_documents"]
        }
        logger.debug(f"Chain response received")
        return response
    except Exception as e:
        logger.exception("Error on query chain")
        raise