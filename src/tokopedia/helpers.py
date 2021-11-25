
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from src.common.selenium import get_selenium_driver


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'


def get_request_raw(url):
    headers = requests.utils.default_headers()
    headers['User-Agent'] = USER_AGENT
    res = requests.get(url, headers=headers)
    if not res.ok:
        raise Exception('Failed to get request products to the Category Page')
    return res.text


def post_gql_request(data):
    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    headers['content-type'] = 'application/json'
    headers['origin'] = 'https://www.tokopedia.com'
    headers['x-tkpd-akamai'] = 'pdpGetLayout'
    headers['x-tkpd-lite-service'] = 'zeus'
    headers['x-device'] = 'desktop'

    res = requests.post(
        'https://gql.tokopedia.com/',
        json=data, headers=headers
    )
    return res.json()[0]


def get_product_data(url):
    url_parsed = urlparse(url)
    if url_parsed.netloc == 'www.tokopedia.com':
        shopdomain, product_key = (
            path for path in url_parsed.path.split('/') if path)
    elif url_parsed.netloc == 'ta.tokopedia.com':
        queries = parse_qs(url_parsed.query)
        if queries.get('r'):
            shopdomain, product_key = (
                path for path in urlparse(queries['r'][0]).path.split('/') if path)
    else:
        return

    res = post_gql_request([
        {
            "operationName": "PDPGetLayoutQuery",
            "variables": {
                "shopDomain": shopdomain,
                "productKey": product_key,
                "layoutID": "",
                "apiVersion": 1,
                "userLocation": {
                    "addressID": "0",
                    "postalCode": "",
                    "latlon": ""
                },
                "extParam": ""
            },
            "query": "fragment ProductVariant on pdpDataProductVariant {\n  errorCode\n  parentID\n  defaultChild\n  sizeChart\n  variants {\n    productVariantID\n    variantID\n    name\n    identifier\n    option {\n      picture {\n        urlOriginal: url\n        urlThumbnail: url100\n        __typename\n      }\n      productVariantOptionID\n      variantUnitValueID\n      value\n      hex\n      __typename\n    }\n    __typename\n  }\n  children {\n    productID\n    price\n    priceFmt\n    optionID\n    productName\n    productURL\n    picture {\n      urlOriginal: url\n      urlThumbnail: url100\n      __typename\n    }\n    stock {\n      stock\n      isBuyable\n      stockWordingHTML\n      minimumOrder\n      maximumOrder\n      __typename\n    }\n    isCOD\n    isWishlist\n    campaignInfo {\n      campaignID\n      campaignType\n      campaignTypeName\n      campaignIdentifier\n      background\n      discountPercentage\n      originalPrice\n      discountPrice\n      stock\n      stockSoldPercentage\n      startDate\n      endDate\n      endDateUnix\n      appLinks\n      isAppsOnly\n      isActive\n      hideGimmick\n      isCheckImei\n      __typename\n    }\n    thematicCampaign {\n      additionalInfo\n      background\n      campaignName\n      icon\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ProductMedia on pdpDataProductMedia {\n  media {\n    type\n    urlThumbnail: URLThumbnail\n    videoUrl: videoURLAndroid\n    prefix\n    suffix\n    description\n    __typename\n  }\n  videos {\n    source\n    url\n    __typename\n  }\n  __typename\n}\n\nfragment ProductHighlight on pdpDataProductContent {\n  name\n  price {\n    value\n    currency\n    __typename\n  }\n  campaign {\n    campaignID\n    campaignType\n    campaignTypeName\n    campaignIdentifier\n    background\n    percentageAmount\n    originalPrice\n    discountedPrice\n    originalStock\n    stock\n    stockSoldPercentage\n    threshold\n    startDate\n    endDate\n    endDateUnix\n    appLinks\n    isAppsOnly\n    isActive\n    hideGimmick\n    __typename\n  }\n  thematicCampaign {\n    additionalInfo\n    background\n    campaignName\n    icon\n    __typename\n  }\n  stock {\n    useStock\n    value\n    stockWording\n    __typename\n  }\n  variant {\n    isVariant\n    parentID\n    __typename\n  }\n  wholesale {\n    minQty\n    price {\n      value\n      currency\n      __typename\n    }\n    __typename\n  }\n  isCashback {\n    percentage\n    __typename\n  }\n  isTradeIn\n  isOS\n  isPowerMerchant\n  isWishlist\n  isCOD\n  isFreeOngkir {\n    isActive\n    __typename\n  }\n  preorder {\n    duration\n    timeUnit\n    isActive\n    preorderInDays\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCustomInfo on pdpDataCustomInfo {\n  icon\n  title\n  isApplink\n  applink\n  separator\n  description\n  __typename\n}\n\nfragment ProductInfo on pdpDataProductInfo {\n  row\n  content {\n    title\n    subtitle\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDetail on pdpDataProductDetail {\n  content {\n    title\n    subtitle\n    applink\n    showAtFront\n    isAnnotation\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDataInfo on pdpDataInfo {\n  icon\n  title\n  isApplink\n  applink\n  content {\n    icon\n    text\n    __typename\n  }\n  __typename\n}\n\nfragment ProductSocial on pdpDataSocialProof {\n  row\n  content {\n    icon\n    title\n    subtitle\n    applink\n    type\n    rating\n    __typename\n  }\n  __typename\n}\n\nquery PDPGetLayoutQuery(\n  $shopDomain: String\n  $productKey: String\n  $layoutID: String\n  $apiVersion: Float\n  $userLocation: pdpUserLocation\n  $extParam: String\n) {\n  pdpGetLayout(\n    shopDomain: $shopDomain\n    productKey: $productKey\n    layoutID: $layoutID\n    apiVersion: $apiVersion\n    userLocation: $userLocation\n    extParam: $extParam\n  ) {\n    name\n    pdpSession\n    basicInfo {\n      alias\n      isQA\n      id: productID\n      shopID\n      shopName\n      minOrder\n      maxOrder\n      weight\n      weightUnit\n      condition\n      status\n      url\n      needPrescription\n      catalogID\n      isLeasing\n      isBlacklisted\n      menu {\n        id\n        name\n        url\n        __typename\n      }\n      category {\n        id\n        name\n        title\n        breadcrumbURL\n        isAdult\n        detail {\n          id\n          name\n          breadcrumbURL\n          isAdult\n          __typename\n        }\n        __typename\n      }\n      txStats {\n        transactionSuccess\n        transactionReject\n        countSold\n        paymentVerified\n        itemSoldPaymentVerified\n        __typename\n      }\n      stats {\n        countView\n        countReview\n        countTalk\n        rating\n        __typename\n      }\n      __typename\n    }\n    components {\n      name\n      type\n      position\n      data {\n        ...ProductMedia\n        ...ProductHighlight\n        ...ProductInfo\n        ...ProductDetail\n        ...ProductSocial\n        ...ProductDataInfo\n        ...ProductCustomInfo\n        ...ProductVariant\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
    ])
    components = res['data']['pdpGetLayout']['components']

    medias = [component for component in components if component['name']
              == 'product_media']
    medias = medias[0]['data'][0]['media'] if medias else []

    content = [
        component for component in components if component['name'] == 'product_content']

    detail = [
        component for component in components if component['name'] == 'product_detail']
    detail = detail[0] if detail else None
    deskripsi = [content for content in detail['data'][0]
                 ['content'] if content['title'] == 'Deskripsi']

    return {
        'name': content[0]['data'][0]['name'],
        'description': deskripsi[0]['subtitle'] if deskripsi else '',
        'images': [media['urlThumbnail'] for media in medias if media.get('urlThumbnail')],
        'price': content[0]['data'][0]['price']['value'],
        'currency': content[0]['data'][0]['price']['currency'],
        'rating': res['data']['pdpGetLayout']['basicInfo']['stats']['rating'],
        'store': res['data']['pdpGetLayout']['basicInfo']['shopName'],
    }


def get_products(category_slug, length=100):
    browser = get_selenium_driver()
    action = ActionChains(browser)
    wait = WebDriverWait(browser, 10)
    browser.get(f'https://www.tokopedia.com/p/{category_slug}')
    products_data = []

    def load_products():
        browser.execute_script("window.scrollTo(0, 5000);")
        action.move_to_element(browser.find_elements_by_css_selector(
            'a[data-testid=lnkProductContainer]')[-1]).perform()
        wait.until(lambda b: len(b.find_elements(By.CSS_SELECTOR,
                   'a[data-testid=lnkProductContainer]')) > 10)

    def load_next_page():
        next_button = browser.find_elements(
            By.CSS_SELECTOR, 'div[data-unify="Pagination"] button')[-1]
        next_button.click()

    def process_products():
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        products_html = soup.select(
            'div[data-testid=lstCL2ProductList] a[data-testid=lnkProductContainer]')[:length]
        for product in products_html:
            products_data.append(get_product_data(product.attrs.get('href')))

    load_products()
    process_products()
    while len(products_data) < length:
        load_next_page()
        load_products()
        process_products()

    browser.close()
    return products_data[:100]
