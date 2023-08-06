from django.core.management.base import CommandError, BaseCommand
from django.apps import apps
from ..base.graph_models import SchemaGenerator

class graph_migrate(BaseCommand):
    help = 'My custom command'

    def handle(self, *args, **options):
        # Get all models from all apps
        models = apps.get_models()

        # Filter models that have a `dgraph_type` attribute
        graph_models = [model for model in models if hasattr(model, 'dgraph_type')]

        # Generate the schema
        schema_generator = SchemaGenerator(graph_models)
        schema = schema_generator.generate_schema()

        # Do something with the schema, like print it to the console
        self.stdout.write(schema)
        
# Register the command
Command = {'mycommand': graph_migrate}
