function fetchProductsByCategory(category) {
    fetch(`/api/products/${category}`)
    .then(response => response.json())
    .then(products => {
        const productsContainer = document.getElementById('products-container');
        productsContainer.innerHTML = ''; 
        products.forEach(product => {
            const productCard = `<div class="product-card">
                                    <a href="/product/${product.id}">
                                        <img src="${product.image_url}" alt="${product.name}">
                                        <h5>${product.name}</h5>
                                        <p>${product.price} TL</p>
                                    </a>
                                 </div>`;
            productsContainer.innerHTML += productCard;
        });
        setActiveCategory(category + '-btn');
    })
    .catch(error => console.error('Error:', error));
}

function loadCategories() {
    fetch('/api/categories')
      .then(response => response.json())
      .then(categories => {
        const categoriesContainer = document.getElementById('categories-container');
        categoriesContainer.innerHTML = '';  
        categories.forEach(category => {
          const categoryButton = document.createElement('button');
          categoryButton.textContent = category;
          categoryButton.classList.add('category-btn');
          categoryButton.id = `${category}-btn`; 
          categoryButton.onclick = function() { 
            fetchProductsByCategory(category); 
            setActiveCategory(`${category}-btn`); 
          };
          categoriesContainer.appendChild(categoryButton);
        });

       
        const defaultCategory = 'Bebek';
        fetchProductsByCategory(defaultCategory);
        setActiveCategory(`${defaultCategory}-btn`); 
      })
      .catch(error => console.error('Error:', error));
  }
  


function setActiveCategory(categoryButtonId) {
    document.querySelectorAll('.category-btn').forEach(button => {
      button.classList.remove('active-category');
    });
    document.getElementById(categoryButtonId).classList.add('active-category');
}

document.addEventListener('DOMContentLoaded', loadCategories);


document.querySelector('.search-box').addEventListener('input', function() {
    searchProducts(); 
});

document.getElementById('sort-order').addEventListener('change', function() {
    searchProducts(); 
});

function searchProducts() {
    const query = document.querySelector('.search-box').value;
    const sortOrder = document.getElementById('sort-order').value;

    if (query.length > 0) {
      fetch(`/api/search?query=${query}&sort=${sortOrder}`)
        .then(response => response.json())
        .then(data => {
          const categoryPanel = document.getElementById('category-panel');
          const productsPanel = document.getElementById('products-panel');
    
          categoryPanel.innerHTML = '';
          data.categories.forEach(cat => {
            const categoryDiv = `<div>${cat.category} (${cat.count})</div>`;
            categoryPanel.innerHTML += categoryDiv;
          });
    
          productsPanel.innerHTML = '';
          data.products.forEach(product => {
            const productCard = `<div class="product-card">
                                    <a href="/product/${product.id}">
                                        <img src="${product.image_url}" alt="${product.name}">
                                        <h5>${product.name}</h5>
                                        <p>${product.price} TL</p>
                                    </a>
                                 </div>`;
            productsPanel.innerHTML += productCard;
          });
          document.getElementById('search-results').style.display = 'block'; 
        })
        .catch(error => console.error('Error:', error));
    } else {
      document.getElementById('search-results').style.display = 'none';  
    }
}

  
function updateSortOrder(order) {
    document.getElementById('sort-order').value = order;
    
     const dropdownItems = document.querySelectorAll('.dropdown-item');
     dropdownItems.forEach(item => {
         if(item.getAttribute('onclick').includes(order)) {
             item.classList.add('selected-option'); 
         } else {
             item.classList.remove('selected-option');
         }
     });
    searchProducts(); 
}


document.addEventListener('DOMContentLoaded', function() {
    updateSortOrder('asc');
});