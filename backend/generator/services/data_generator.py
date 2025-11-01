from faker import Faker

class DataGenerator:
    """
    A service class responsible for initializing the Faker library and 
    generating synthetic data records based on a defined schema.
    """
    def __init__(self, locale='fr_FR'):
        """
        Initializes the Faker generator instance.

        Args:
            locale (str): The localization code to use for data generation
                          (e.g., 'en_US', 'fr_FR'). Defaults to 'fr_FR'.
        """
        self.fake = Faker(locale)
    
    def generate_field(self, field_type):
        """
        Generates a single data value based on the requested field type.
        
        It uses a dictionary mapping to call the appropriate Faker provider method.
        
        Args:
            field_type (str): The type of data to generate (e.g., 'name', 'email', 'custom_text(50)').

        Returns:
            str: The generated fake data value.
        """
        # Dictionary mapping field type strings to their respective Faker methods (using lambda for lazy execution)
        generators = {
            'name': lambda: self.fake.name(),
            'first_name': lambda: self.fake.first_name(),
            'last_name': lambda: self.fake.last_name(),
            'email': lambda: self.fake.email(),
            'phone_number': lambda: self.fake.phone_number(),
            'address': lambda: self.fake.address(),
            'country': lambda: self.fake.country(),
            'city': lambda: self.fake.city(),
            'date': lambda: self.fake.date(),
            'datetime': lambda: self.fake.date_time().isoformat(),
            'company': lambda: self.fake.company(),
            'job': lambda: self.fake.job(),
            'iban': lambda: self.fake.iban(),
            'credit_card': lambda: self.fake.credit_card_number(),
            'license_plate': lambda: self.fake.license_plate(),
            'text': lambda: self.fake.text(max_nb_chars=200),
            'paragraph': lambda: self.fake.paragraph(),
            'url': lambda: self.fake.url(),
            'ipv4': lambda: self.fake.ipv4(),
            'user_agent': lambda: self.fake.user_agent(),
        }
        
        # --- Custom Text Length Handling ---
        # Checks if the type is a custom text request (e.g., "custom_text(50)")
        if field_type.startswith('custom_text'):
            try:
                # Extracts the desired length from the string using simple parsing
                length = int(field_type.split('(')[1].split(')')[0])
                return self.fake.text(max_nb_chars=length)
            except:
                # Fallback to a default text length if parsing fails
                return self.fake.text(max_nb_chars=100)
        
        # Retrieves the generator function from the dictionary
        generator = generators.get(field_type)
        if generator:
            return generator()
        else:
            return f"Unknown type: {field_type}"
    
    def generate_dataset(self, schema, num_rows):
        """
        Generates a complete list of records (dataset) based on the schema and row count.
        
        Args:
            schema (dict): The dictionary defining the field_name: field_type structure.
                           Example: {"name": "name", "email": "email", "country": "country"}
            num_rows (int): The number of records to generate.

        Returns:
            list: A list of dictionaries, where each dictionary is a generated row.
        """
        dataset = []
        # Loop for the specified number of rows
        for _ in range(num_rows):
            row = {}
            # Iterate through the schema to generate data for each field
            for field_name, field_type in schema.items():
                row[field_name] = self.generate_field(field_type)
            dataset.append(row)
        return dataset