**Steps to Migrate DB using Alembic**

1. Initialize the alembic using the command.
   ```
   alembic init alembic
   ```
2. Then enable the fileConfig without having any condition in `alembic/env.py`
    ```
   # if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    ```
3. Afterwards, add the `target_metadata` as Base metadata
   ```
    target_metadata = Base.metadata
   ```
4. Update the sqlalchemy url in `alembic.ini` with your local db set up
    ```
    sqlalchemy.url = postgresql+psycopg2://postgres:<your-db-pasword>@localhost:5433/<db-name>
   ```
5. Add the changes you want to make in your database models
    ```
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
    ```
6. Then commit the alembic revision so that versions can get generated
    ```
    alembic revision -m "Include updated_at column for todos table"  
    ```
7. Now, you would get this changes as versions in `alembic/versions/f48f5c6aadea_include_updated_at_column_for_todos_.py`
8. Then you could open this version and define the upgrade & downgrade function for making the updates & reverting it respectively
9. In this case, upgrade add a new column `updated_at` & downgrade drop that newly created column
    ```
    def upgrade() -> None:
        """Upgrade schema."""
        op.add_column("todos",
              sa.Column(
                  "updated_at",
                  sa.DateTime(timezone=True),
                    onupdate=sa.text("NOW()")
              )
        )


    def downgrade() -> None:
        """Downgrade schema."""
        op.drop_column("todos", "updated_at")
    ```
10. Then finally upgrade the database model changes to live
    ```
        alembic upgrade <revision-id>
    ```
11. You can identify the revision id from `alembic/versions/f48f5c6aadea_include_updated_at_column_for_todos_.py`