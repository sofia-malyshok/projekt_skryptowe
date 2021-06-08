import tkinter as tk
from tkinter.filedialog import asksaveasfile
import requests
from PIL import Image, ImageTk
from io import BytesIO

WINDOW_TITLE = 'Recipe app'
API_URL = 'https://api.spoonacular.com/recipes'
API_KEY = '32bd8b17f0164b938752d6970742006b'

class RecipeApp():
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg='#fff')
        self.root.geometry('1100x750')
        self.root.title('Recipe app')

        self.BUTTON_HOLDER = tk.PhotoImage(file='./assets/button.png')

        self.header_frame = tk.Frame(self.root, padx=30, pady=15)
        self.body_frame = tk.Frame(self.root, padx=30, pady=15)
        self.menu = tk.Menu(self.root)

        self.recipe = None
        self.query = 'Start searching recipes'

        self.display_header()
        self.display_body()
        self.display_menu()

    def display_header(self):
        self.entry = tk.Entry(self.header_frame)
        self.entry.grid(row=0, column=0, sticky=tk.NSEW)
        self.entry.insert(0, self.query)
        self.entry.bind('<FocusIn>', self.clear_entry)

        self.search_button = tk.Button(self.header_frame, text='Search', font=('Rockwell', 12), image=self.BUTTON_HOLDER, border=0, borderwidth=0, bg='#fff', fg='#fff', highlightbackground='#fff', highlightthickness = 0, bd = 0, activebackground='#fff', activeforeground='#fff', compound='center', command=self.search_recipes)
        self.search_button.grid(row=0, column=1)

        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.pack(fill='x')
    
    def display_body(self):
        holder_image = Image.open('./assets/holder.png')
        holder_image = holder_image.resize((600, 600))
        holder = ImageTk.PhotoImage(holder_image)
        holder_label = tk.Label(self.body_frame, image=holder)
        holder_label.grid(row=0, column=0)
        holder_label.image = holder

        self.body_frame.grid_columnconfigure(0, weight=1)
        self.body_frame.pack(fill='x')
    
    def display_menu(self):
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='File', menu=file_menu, state=tk.DISABLED)
        file_menu.add_command(label='Save recipe', command=self.save_recipe)

        self.root.config(menu=self.menu)
    
    def clear_entry(self, e):
        self.entry.delete(0, tk.END)

    def clear_frame(_self, frame): 
        for widget in frame.winfo_children():
            widget.destroy()

        frame.pack_forget()

    def search_recipes(self):
        self.clear_frame(self.body_frame)
        self.query = self.entry.get() or self.query
        recipes = self.fetch_recipes(self.query)

        for recipe in recipes:
            self.display_recipes_item(recipe)

        self.body_frame.pack(fill='x')
        self.menu.entryconfigure(1, state=tk.DISABLED)

    # return data with basic information about recipes from API
    def fetch_recipes(self, query):
        response = requests.get('{0}/complexSearch?apiKey={1}&query={2}&number=4'.format(API_URL, API_KEY, query))

        return response.json()['results']

    # show list of recipes with basic information on screen
    def display_recipes_item(self, recipe):
        recipe_frame = tk.Frame(self.body_frame, pady=15, bg='#fff')

        image = Image.open(BytesIO(requests.get(recipe['image']).content))
        image = image.resize((155, 115))
        image = ImageTk.PhotoImage(image)
        image_block = tk.Label(recipe_frame, image=image, borderwidth=0)
        image_block.grid(row=0, column=0, rowspan=2)
        image_block.image = image

        label = tk.Label(recipe_frame, text=recipe['title'], font=('Rockwell', 22), bg='#fff')
        label.grid(row=0, column=1, sticky=tk.SW, padx=10)

        button = tk.Button(recipe_frame, text='See more', font=('Rockwell', 12), image=self.BUTTON_HOLDER, border=0, borderwidth=0, bg='#fff', fg='#fff', highlightbackground='#fff', highlightthickness = 0, bd = 0, activebackground='#fff', activeforeground='#fff', compound='center', command=lambda: self.search_recipe(recipe['id']))
        button.grid(row=1, column=1, sticky=tk.SW, padx=10)

        recipe_frame.pack(fill='x')

    def search_recipe(self, id):
        self.clear_frame(self.body_frame)
        self.fetch_recipe(id)
        self.display_recipe()

        self.body_frame.grid_columnconfigure(1, weight=1)
        self.body_frame.grid_columnconfigure(2, weight=1)
        self.body_frame.pack(fill='x')

        self.menu.entryconfigure(1, state=tk.NORMAL)

    # return data with information about chosen recipe from API
    def fetch_recipe(self, id):
        response = requests.get('{0}/{1}/information?apiKey={2}'.format(API_URL, id, API_KEY))
        recipe = response.json()

        instruction = self.fetch_instruction(id)
        instruction_str = 'Instruction:\n\n'

        for index in range(len(instruction)):
            instruction_str += '{0}. {1}\n'.format(index + 1, instruction[index])

        self.recipe = {
            'title': recipe['title'],
            'image': recipe['image'],
            'ready_in_minutes': '{0} min'.format(recipe['readyInMinutes']),
            'dish_types': recipe['dishTypes'][0:2],
            'ingredients': list(map(lambda ingredient: ingredient['original'], recipe['extendedIngredients'])),
            'instruction': instruction_str,
        }

    # return data with instruction of chosen recipe from API
    def fetch_instruction(self, id):
        response = requests.get('{0}/{1}/analyzedInstructions?apiKey={2}'.format(API_URL, id, API_KEY))
        instruction = response.json()[0]['steps'] if len(response.json()) else [{ 'step': 'No instruction' }]
        return list(map(lambda item: item['step'], instruction))

    # show detailed information about chosen recipe on screen
    def display_recipe(self):
        label = tk.Label(self.body_frame, text=self.recipe['title'], font=('Rockwell', 22), bg='#fff')
        label.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        image = Image.open(BytesIO(requests.get(self.recipe['image']).content))
        image = image.resize((400, 260))
        image = ImageTk.PhotoImage(image)
        image_block = tk.Label(self.body_frame, image=image, border=0, borderwidth=0)
        image_block.grid(row=1, column=0, rowspan=3, padx=(0, 30), sticky=tk.NW)
        image_block.image = image

        type = tk.Label(self.body_frame, text=', '.join(self.recipe['dish_types']), font=('Rockwell', 16), bg='#fff', fg="#acada8")
        type.grid(row=1, column=1, sticky=tk.NW)

        time = tk.Label(self.body_frame, text=self.recipe['ready_in_minutes'], font=('Rockwell', 16), bg='#fff', fg="#acada8")
        time.grid(row=1, column=2, sticky=tk.NE)

        ingredients_title = tk.Label(self.body_frame, text='Ingredients', font=('Rockwell', 18), bg='#fff')
        ingredients_title.grid(row=2, column=1, columnspan=2, pady=(20, 10), sticky=tk.EW)

        ingredients = tk.Text(self.body_frame, font=('Rockwell', 16), height=7, highlightbackground='#fff', highlightthickness = 0, bd = 0, bg='#fff')
        ingredients.insert(tk.END, '\n'.join(self.recipe['ingredients']))
        ingredients.config(state=tk.DISABLED)
        ingredients.grid(row=3, column=1, columnspan=2, sticky=tk.NSEW)

        instruction = tk.Text(self.body_frame, font=('Rockwell', 16), height=12, highlightbackground='#fff', highlightthickness = 0, bd = 0, bg='#fff')
        instruction.insert(tk.END, self.recipe['instruction'])
        instruction.config(state=tk.DISABLED)
        instruction.grid(row=4, column=0, columnspan=3, pady=30, sticky=tk.EW)

        back_button = tk.Button(self.body_frame, text='Back to search', font=('Rockwell', 12), image=self.BUTTON_HOLDER, border=0, borderwidth=0, bg='#fff', fg='#fff', highlightbackground='#fff', highlightthickness = 0, bd = 0, activebackground='#fff', activeforeground='#fff', compound='center', command=self.search_recipes)
        back_button.grid(row=5, column=0, columnspan=3, sticky=tk.E)

    def save_recipe(self):
        file = asksaveasfile(initialfile='recipe.txt', defaultextension='.txt', filetypes=[('Text Documents', '*.txt')])
        
        if not(file):
            return 

        recipe_data = '{0}\n\nDish types: {1}\nTime for cooking: {2}\n\nIngredients:\n\n{3}\n\n{4}'.format(
            self.recipe['title'],
            ', '.join(self.recipe['dish_types']),
            self.recipe['ready_in_minutes'],
            '\n'.join(self.recipe['ingredients']),
            self.recipe['instruction'],
        )
        
        file.write(recipe_data)
        file.close()

    def run_app(self):
        self.root.mainloop()

if __name__ == '__main__':
    recipe_app = RecipeApp()
    recipe_app.run_app()
    