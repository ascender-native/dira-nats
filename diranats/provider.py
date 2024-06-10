from diracore.contracts.foundation.application import Application
from diracore.foundation.application import Application
from diracore.support.service_provider import ServiceProvider
from diracore.routing.router import Router
from diracore.main import config

from diracore.foundation.console.console_kernel import ConsoleKernel


class NatsServiceProvider(ServiceProvider):
    
    # Composite service provider to register all necessary components for the bot
    async def register(self):
        if isinstance(self.kernel, ConsoleKernel):
            self.register_console()

        self.publish({'diranats.config.nats': 'config.nats'}, 'config')
        
    
    def register_console(self):
        # Load the console module into the kernel
        self.kernel.load('diranats.console')