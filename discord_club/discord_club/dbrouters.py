class ModelSpecificRouter(object):
    def db_for_read(self, model, **hints):
        """Send all read operations on Example app models to `example_db`."""
        return getattr(model, "_db", None)

    def db_for_write(self, model, **hints):
        """Send all write operations on Example app models to `example_db`."""
        return getattr(model, "_db", None)

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the Example app's models get created on the right database."""
        return None
