from loguru import logger

from app.workflow import create_workflow, create_graph_png


if __name__ == "__main__":
    input = {
        "messages": [
            "What is the conversion factor between USD and INR, and based on that can you convert 10 USD to INR"
        ]
    }

    app = create_workflow()
    # create_graph_png(app)

    resp = app.invoke(input)
    answer = resp["messages"][-1]
    logger.debug(answer.content)
