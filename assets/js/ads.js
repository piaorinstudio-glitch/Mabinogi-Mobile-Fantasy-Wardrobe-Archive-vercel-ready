(()=>{
  const cfg=window.MABI_ADS_CONFIG||{};
  if(!cfg.enabled||!cfg.client)return;
  if(document.querySelector('script[data-mabi-adsense]'))return;
  const script=document.createElement('script');
  script.async=true;
  script.crossOrigin='anonymous';
  script.dataset.mabiAdsense='1';
  script.src=`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${encodeURIComponent(cfg.client)}`;
  document.head.appendChild(script);
})();
