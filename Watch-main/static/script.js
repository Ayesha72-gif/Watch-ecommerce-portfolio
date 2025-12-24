/* ==============================menubar js================*/
const navbarToggle=document.querySelector('.navbar_toggle')
const menuBar=document.querySelector('.menu_bar')
navbarToggle.addEventListener('click',() => {
menuBar.classList.toggle("active");
  navbarToggle.classList.toggle("active");
})


/* ========searchbar javascript-------------*/
 const btn =document.getElementById('search-btn')
  const box =document.getElementById('search-box')
  const input =document.getElementById('search-input')
  btn.addEventListener('click', () =>{
    box.classList.toggle('show');
    if(box.classList.contains('show')){
        setTimeout(() => input.focus(), 150)
    }
    });
    input.addEventListener('keydown', function(e){
        if(e.key =='Enter'){
            const query=input.value.trim();
            box.classList.remove('show')
            input.value =="";
        if (query!= ""){
            window.location.href ="/search/?query=" + encodeURIComponent(query);
        }
        }
    })