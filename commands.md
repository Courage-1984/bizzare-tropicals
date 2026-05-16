
npm install -g @shopify/cli@latest

shopify theme init carnivorous-plants-theme

cd carnivorous-plants-theme

shopify theme dev --store your-store-name.myshopify.com
shopify theme dev --store bizzare-tropicals.myshopify.com

shopify auth logout
shopify auth login
shopify theme dev --store bizzare-tropicals-2.myshopify.com


git init
git add .
git commit -m "Initial Dawn clone"

git remote add origin https://github.com/Courage-1984/bizzare-tropicals.git


