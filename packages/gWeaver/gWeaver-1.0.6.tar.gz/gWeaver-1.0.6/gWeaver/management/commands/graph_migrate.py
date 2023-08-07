from django.core.management.base import CommandError, BaseCommand
from django.apps import apps
from ...base.schema_generator import SchemaGenerator

class Command(BaseCommand):
    help = 'Generate a Dgraph schema based on the models in your project.'

    def handle(self, *args, **options):
        # Get all models from all apps
        models = apps.get_models()

        # Filter models that have a `dgraph_type` attribute
        graph_models = [model for model in models if hasattr(model, 'dgraph_type')]

        # Generate the schema
        schema_generator = SchemaGenerator(graph_models)
        
        schema = schema_generator.generate_dgraph_schema()
        print(schema)
        schema_generator.post_to_dgraph()
        # write schema to a file 
        with open('schema.txt', 'w') as f:
            f.write(schema)
        self.stdout.write(
                self.style.SUCCESS('Successfully created schema for Dgraph.')
        )
