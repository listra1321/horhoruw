from agents import UnifiedAgent

class AgentOrchestrator:

    def __init__(self):

        self.agent = UnifiedAgent()

    def run(self, text, caption, destination):

        return self.agent.run(
            text,
            caption,
            destination
        )
