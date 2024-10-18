
function isFullScreen() {
    return (
        document.fullscreenElement ||
        document.webkitFullscreenElement ||
        document.mozFullScreenElement ||
        document.msFullscreenElement
    );
}

function preventFullScreen() {
    if (isFullScreen()) {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }}
}

function noFullScreen(){
    document.addEventListener('fullscreenchange', preventFullScreen);
    document.addEventListener('webkitfullscreenchange', preventFullScreen);
    document.addEventListener('mozfullscreenchange', preventFullScreen);
    document.addEventListener('MSFullscreenChange', preventFullScreen);
}

function displayToast(type, color, message) {
    var link = document.createElement('link');
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css';
    link.rel = 'stylesheet';
    link.type = 'text/css';
    document.head.appendChild(link);

    if (color == 'green') { 
        color = '#478547'; 
    } else { 
        color = 'red'; 
    }
    
    var toast = document.createElement('div');
    toast.classList.add('toast');

    var textcap = document.createTextNode(message);

    var icon = document.createElement('i');
    icon.classList.add('fa', 'fa-' + type);
    icon.setAttribute('aria-hidden', 'true');
    icon.style.fontSize = '20px';
    icon.style.position = 'absolute';
    icon.style.left = '0';
    icon.style.marginLeft = '10px';
    icon.style.marginRight = '10px';
    icon.style.color = color;

    toast.appendChild(icon);
    toast.appendChild(textcap);

    document.body.appendChild(toast);

    toast.style.position = 'fixed';
    toast.style.top = '0px';
    toast.style.left = '50%';
    toast.style.transform = 'translateX(-50%) translateY(-100%)';
    toast.style.backgroundColor = 'rgba(250, 250, 250)';
    toast.style.color = color;
    toast.style.padding = '10px 40px';
    toast.style.borderRadius = '3px';
    toast.style.borderLeft = `10px solid ${color}`;
    toast.style.zIndex = '9999';
    toast.style.fontWeight = 'bold';
    toast.style.fontFamily = 'Arial, sans-serif';
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.5s, transform 0.5s';
    toast.style.boxShadow = '0 4px 8px rgba(0, 0, 0, .5)';
    toast.style.textAlign = 'center';
    toast.style.alignItems = 'center';
    toast.style.display = 'flex';
    toast.style.maxWidth = '250px';
    toast.style.minWidth = 'fit-content';

    setTimeout(function() {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(-50%) translateY(20px)';
    }, 10);

    setTimeout(function() {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-50%) translateY(-100%)';
        toast.addEventListener('transitionend', function() {
            toast.remove();
        });
    }, 2000);
}

function highlightClick(x, y) {
    var clickIndicator = document.createElement('div');
    clickIndicator.style.position = 'absolute';
    clickIndicator.style.top = y + 'px';
    clickIndicator.style.left = x + 'px';
    clickIndicator.style.width = '20px';
    clickIndicator.style.height = '20px';
    clickIndicator.style.backgroundColor = '#39FF14';
    clickIndicator.style.borderRadius = '50%';
    clickIndicator.style.zIndex = '9999';
    clickIndicator.style.opacity = '0.8';
    clickIndicator.style.pointerEvents = 'none';
    clickIndicator.style.transition = 'opacity 0.5s ease-out';
    document.body.appendChild(clickIndicator);
    setTimeout(function() {
        clickIndicator.style.opacity = '0';
        setTimeout(function() {
            document.body.removeChild(clickIndicator);
        }, 500);
    }, 500);
}