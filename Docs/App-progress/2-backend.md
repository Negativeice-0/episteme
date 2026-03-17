# Backend is being a pain

But i then realized that my prompt was not all that.

Regardless we try again with some note from the past.

Now the setup is very important.

Ensure you have python 3.10 -- as of march 17 - 2026 it is the most stable and will avoid distutil errors.

Maybe in 2027 you can use the now current version 3.12. -- If on linux finding 3.10 might be hard so instead use dead snakes ppa repo. After which you can install python3.10, python 3.10 pip cli, python3.10 dev -y, etc.

THen use it to create the virtual environment and you are good.

```bash
python3.10 -m venv venv

# next

source venv/bin/activate

# next

pip install -r requirements.txt

```
