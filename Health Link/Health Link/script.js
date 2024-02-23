let menu = document.querySelector('#menu-bars');
let header = document.querySelector('header')
menu.onclick = () =>{
    menu.classList.toggle('fa-times');
    header.classList.toggle('active');
}
window.onscroll = () =>{
    menu.classList.remove('fa-times');
    header.classList.remove('active');
}
let cursor1 = document.querySelector('.cursor-1');
let cursor2 = document.querySelector('.cursor-2');
window.onmousemove = (e) =>{
    cursor1.style.top = e.pageY + 'px';
    cursor1.style.left = e.pageX + 'px';
    cursor2.style.top = e.pageY + 'px';
    cursor2.style.left = e.pageX + 'px';
}
document.querySelectorAll('a').forEach(links =>{
    links.onmouseenter = () =>{
        cursor1.classList.add('active');
        cursor1.classList.add('active');
    }
    links.onmouseleave = () =>{
        cursor1.classList.remove('active');
        cursor2.classList.remove('active');
    }
});

window.onload = function() {
  var portfolioImage1 = document.getElementsByClassName('portfolio-image1');
  
  for (var i = 0; i < portfolioImage1.length; i++) {
    var imageData1 = localStorage.getItem('portfolioImage1');
    if (imageData1) {
      portfolioImage1[i].src = imageData1;
    } else {
      portfolioImage1[i].style.display = 'none';
    }
  }
};
