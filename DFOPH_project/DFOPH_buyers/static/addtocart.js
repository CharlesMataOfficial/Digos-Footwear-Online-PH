const product = [
    {
        id: 0,
        image: 'https://image-cdn.hypb.st/https%3A%2F%2Fhypebeast.com%2Fimage%2F2021%2F07%2Fnike-giannis-immortality-championship-greek-freak-celebratory-shoe-cz4099-100-001.jpg?q=75&w=800&cbr=1&fit=max',
        title: 'Giannis Immortality',
        price: 4320,
    },
    {
        id: 1,
        image: 'https://static.nike.com/a/images/w_1280,q_auto,f_auto/e731451e-39ff-45ce-84dc-69d4e88f17bb/kobe-v-protro-big-stage-release-date.jpg',
        title: 'Nike Zoom Kobe 5 ProTro',
        price: 6300,
    },
    {
        id: 2,
        image: 'https://images.solecollector.com/complex/images/c_crop,h_1047,w_1861,x_0,y_30/c_fill,dpr_2.0,f_auto,fl_lossy,q_auto,w_800/xgj06aanxvbw7khgjdrf/adidas-dame-7-navy-lateral',
        title: 'Adidas Dame 7',
        price: 4200,
    },
    {
        id: 3,
        image: 'https://cdn.runrepeat.com/i/adidas/36657/adidas-unisex-dame-7-basketball-shoe-black-none-silver-metallic-13-us-men-black-none-silver-metallic-9ccb-380.jpg',
        title: 'Adidas Dame Dolla 7 Rose',
        price: 4200,
    },
    {
        id: 4,
        image: 'https://d3pnpe87i1fkwu.cloudfront.net/IMG/016350-jordan-luka-1-dn1772-104_1170x1170.png',
        title: 'Luka 1',
        price: 4230,
    },
    {
        id: 5,
        image: 'https://image.goat.com/1000/attachments/product_template_pictures/images/082/557/739/original/1101605_00.png.png',
        title: 'Curry Flow 10 Northern Lights',
        price: 6600,
    },
    
];
const categories = [...new Set(product.map((item)=>
    {return item}))]
    let i=0;
document.getElementById('root').innerHTML = categories.map((item)=>
{
    var {image, title, price} = item;
    return(
        `<div class='box'>
            <div class='img-box'>
                <img class='images' src=${image}></img>
            </div>
        <div class='bottom'>
        <p>${title}</p>
        <h2>P ${price}.00</h2>`+
        "<button onclick='addtocart("+(i++)+")'>Add to cart</button>"+
        `</div>
        </div>`
    )
}).join('')

var cart =[];

function addtocart(a){
    cart.push({...categories[a]});
    displaycart();
}
function delElement(a){
    cart.splice(a, 1);
    displaycart();
}

function displaycart(){
    let j = 0, total=0;
    document.getElementById("count").innerHTML=cart.length;
    if(cart.length==0){
        document.getElementById('cartItem').innerHTML = "Your cart is empty";
        document.getElementById("total").innerHTML = "P "+0+".00";
    }
    else{
        document.getElementById("cartItem").innerHTML = cart.map((items)=>
        {
            var {image, title, price} = items;
            total=total+price;
            document.getElementById("total").innerHTML = "P "+total+".00";
            return(
                `<div class='cart-item'>
                <div class='row-img'>
                    <img class='rowimg' src=${image}>
                </div>
                <p style='font-size:12px;'>${title}</p>
                <h2 style='font-size: 15px;'>P ${price}.00</h2>`+
                "<i class='fa-solid fa-trash' onclick='delElement("+ (j++) +")'></i></div>"
            );
        }).join('');
    }

    
}
const placeOrderButton = document.querySelector('input[type="submit"]');

placeOrderButton.addEventListener('click', function() {
  alert('Thank you for ordering, your package will arrive shortly.');
});