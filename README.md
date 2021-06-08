# Recipe application

Recipe application is desktop application, written on Python, using library Tkinter. This app allows to search different recipes and save them on computer as a text file.

## Constructor

```python
def __init__(self):
```
All main elements of Tkinter application are defined in constructor:

* `main window`
* `head frame`
* `body frame`
* `menu`

There are also 3 functions called in constructor, which display head frame, body frame and menu

```python
self.display_header()
self.display_body()
self.display_menu()
```

## Methods

```python
def display_header(self):
    ...
```

This method is used for displaying `header frame` in main window. There are such Tkinter elments as `Entry` and `Button` in header frame, which are used as input and button for searching. These elements are placed on header frame using `grid`.  

<br>

```python
def display_body(self):
    ...
```

This method is used for displaying `body frame` in main window. There is such Tkinter elments as `Label` in body frame, which is used for placing `holder_image ` on start screen. This label is placed on body frame using `grid`.  

<br>

```python
def display_menu(self):
    ...
```
This method is used for displaying `menu` in main window. Firstly, Tkinter element `Menu` is created and saved in variable which is called `file_menu`, then it replaces the default Tkinter menu and `Save` command(for saving recipes in text file) is added.

<br>

```python
def clear_entry(self, e):
    self.entry.delete(0, tk.END)
```
This method takes one parameter `e` - an `Entry` element which must be cleared.

<br>

```python
def clear_frame(sel, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        frame.pack_forget()
```
This method takes one parameter `frame` - a `Frame` element which must be cleared. In a loop all widgets which are placed in a `frame` are destroyed and all configurations of `frame` are deleted.

<br>

```python
def fetch_recipes(self, query):
    ...
```
This method takes one parameter `query` - key word for searching. In this method the request to the API is done for searching recepies according  key word . This method returns 4 suitable results in json format.

<br>

```python
def display_recipes_list(self, recipe):
    ...
```
This method takes one parameter `recipe` - object with basic information. In this method image, title and button for getting more information about recipe are placed on `recipe_frame` (Frame element, placed on `body_frame`).

<br>

```python
def search_recipes(self):
    ...
```
Firstly in this method `body_frame ` is cleared, then query from input Entry is taken and passed to `fetch_recipes` method as argument, the result of calling this method is written to `recipes` variable, then in a loop it is iterated and  information about each founded recipe is displayed by calling `display_recipes_list` method and passing to it every iterating element as argument.

<br>

```python
def fetch_recipe(self, id):
    ...
```
This method takes one parameter `id` - which is id of choosen recipe. In this method the request to the API is done for searching title, image, time for cooking and ingredients about recipe with special id. Also function `fetch_instruction` is called to get insruction of recipe with choosen id. All founded informations are formated and saved as object to the field `recipe`.

<br>

```python
def fetch_instruction(self, id):
    ...
```
This method takes one parameter `id` - which is id of choosen recipe. In this method the request to the API is done for searching instruction with steps about rchoosen recipe. Method returns list of steps for founded instruction.

<br>

```python
def display_recipe(self):
    ...
```
This method is for displaying choosen recipe on screen.
* title ,image, dish type, time for cooking are placed on different Label elements 
* ingredients and instruction are placed on different Text elements
* button for backing to search is Button element

Al these elements are placed in `body_frame`, using `grid`

<br>

```python
def search_recipe(self, id):
    ...
```
Firstly in this method `body_frame ` is cleared, then `fetch_recipe` and `display_recipe` methods are called. As a result detailed information about choosen recipe is displayed.

<br>

```python
def save_recipe(self):
    ...
```
This method is for saving choosen recipe in txt file. The data which is contains in `recipe` field is formating and writtem to txt file.

<br>

```python
def run_app(self):
    ...
```
Method for running application
