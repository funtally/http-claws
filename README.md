# Interactive HTTP Cats
Turn learning HTTP status codes into a fun and interactive game with [http.cat](https://http.cat)!

# Fun Facts

Did you know that the cat images on http.cat aren't perfectly uniform?

Every http.cat image has a surrounding frame:

![302.jpg](.purrr_cache/302.jpg)

The frames' edges vary not only in their distance from the image edges but also slightly in size. Here's a snapshot of some of these variations:

| HTTP Code | Distance From Left (px) | Distance From Right (px) | Original Image                       | Cropped Image               |
|-----------|-------------------------|--------------------------|--------------------------------------|-----------------------------|
| 103.jpg   | 69                      | 67                       | [103.jpg](.purrr_cache/103.jpg)       | [103.jpg](cats/103.jpg)     |
| 208.jpg   | 55                      | 53                       | [208.jpg](.purrr_cache/208.jpg)       | [208.jpg](cats/208.jpg)     |
| 226.jpg   | 55                      | 53                       | [226.jpg](.purrr_cache/226.jpg)       | [226.jpg](cats/226.jpg)     |
| 414.jpg   | 129                     | 105                      | [414.jpg](.purrr_cache/414.jpg)       | [414.jpg](cats/414.jpg)     |
| 407.jpg   | 69                      | 67                       | [407.jpg](.purrr_cache/407.jpg)       | [407.jpg](cats/407.jpg)     |
| 203.jpg   | 69                      | 67                       | [203.jpg](.purrr_cache/203.jpg)       | [203.jpg](cats/203.jpg)     |
| 428.jpg   | 69                      | 67                       | [428.jpg](.purrr_cache/428.jpg)       | [428.jpg](cats/428.jpg)     |

This quirky irregularity inspired the development of a precise algorithm to dynamically identify and crop the frames around these charming cats—down to the pixel.

To achieve this, we strategically scan selected pixels to locate the frame edges without examining the entire image. This makes the algorithm both efficient and adaptable, allowing for pixel-perfect cropping without relying on predefined margins.

Below is a table showing how many pixels were examined to dynamically find the frame for each HTTP status code:

| HTTP Code | Cat Image Dimensions | Pixels Examined | Original Image                       | Cropped Image               |
|-----------|----------------------|-----------------|--------------------------------------|-----------------------------|
| 100       | 750x600              | 334             | [100.jpg](.purrr_cache/100.jpg)       | [100.jpg](cats/100.jpg)     |
| 101       | 750x600              | 334             | [101.jpg](.purrr_cache/101.jpg)       | [101.jpg](cats/101.jpg)     |
| 102       | 750x600              | 334             | [102.jpg](.purrr_cache/102.jpg)       | [102.jpg](cats/102.jpg)     |
| 103       | 750x600              | 333             | [103.jpg](.purrr_cache/103.jpg)       | [103.jpg](cats/103.jpg)     |
| 200       | 750x600              | 334             | [200.jpg](.purrr_cache/200.jpg)       | [200.jpg](cats/200.jpg)     |
| 201       | 750x600              | 334             | [201.jpg](.purrr_cache/201.jpg)       | [201.jpg](cats/201.jpg)     |
| 202       | 750x600              | 334             | [202.jpg](.purrr_cache/202.jpg)       | [202.jpg](cats/202.jpg)     |
| 203       | 750x600              | 333             | [203.jpg](.purrr_cache/203.jpg)       | [203.jpg](cats/203.jpg)     |
| 204       | 750x600              | 334             | [204.jpg](.purrr_cache/204.jpg)       | [204.jpg](cats/204.jpg)     |
| 205       | 600x750              | 351             | [205.jpg](.purrr_cache/205.jpg)       | [205.jpg](cats/205.jpg)     |
| 206       | 600x750              | 302             | [206.jpg](.purrr_cache/206.jpg)       | [206.jpg](cats/206.jpg)     |
| 207       | 750x600              | 334             | [207.jpg](.purrr_cache/207.jpg)       | [207.jpg](cats/207.jpg)     |
| 208       | 600x750              | 351             | [208.jpg](.purrr_cache/208.jpg)       | [208.jpg](cats/208.jpg)     |
| 226       | 600x750              | 351             | [226.jpg](.purrr_cache/226.jpg)       | [226.jpg](cats/226.jpg)     |
| 300       | 600x750              | 302             | [300.jpg](.purrr_cache/300.jpg)       | [300.jpg](cats/300.jpg)     |
| 301       | 750x600              | 334             | [301.jpg](.purrr_cache/301.jpg)       | [301.jpg](cats/301.jpg)     |
| 302       | 750x600              | 334             | [302.jpg](.purrr_cache/302.jpg)       | [302.jpg](cats/302.jpg)     |
| 303       | 750x600              | 334             | [303.jpg](.purrr_cache/303.jpg)       | [303.jpg](cats/303.jpg)     |
| 304       | 600x750              | 302             | [304.jpg](.purrr_cache/304.jpg)       | [304.jpg](cats/304.jpg)     |
| 305       | 750x600              | 334             | [305.jpg](.purrr_cache/305.jpg)       | [305.jpg](cats/305.jpg)     |
| 307       | 600x750              | 302             | [307.jpg](.purrr_cache/307.jpg)       | [307.jpg](cats/307.jpg)     |
| 308       | 750x600              | 334             | [308.jpg](.purrr_cache/308.jpg)       | [308.jpg](cats/308.jpg)     |
| 400       | 750x600              | 334             | [400.jpg](.purrr_cache/400.jpg)       | [400.jpg](cats/400.jpg)     |
| 401       | 750x600              | 334             | [401.jpg](.purrr_cache/401.jpg)       | [401.jpg](cats/401.jpg)     |
| 402       | 750x600              | 334             | [402.jpg](.purrr_cache/402.jpg)       | [402.jpg](cats/402.jpg)     |
| 403       | 750x600              | 334             | [403.jpg](.purrr_cache/403.jpg)       | [403.jpg](cats/403.jpg)     |
| 404       | 750x600              | 334             | [404.jpg](.purrr_cache/404.jpg)       | [404.jpg](cats/404.jpg)     |
| 405       | 750x600              | 334             | [405.jpg](.purrr_cache/405.jpg)       | [405.jpg](cats/405.jpg)     |
| 406       | 750x600              | 334             | [406.jpg](.purrr_cache/406.jpg)       | [406.jpg](cats/406.jpg)     |
| 407       | 750x600              | 333             | [407.jpg](.purrr_cache/407.jpg)       | [407.jpg](cats/407.jpg)     |
| 408       | 750x600              | 334             | [408.jpg](.purrr_cache/408.jpg)       | [408.jpg](cats/408.jpg)     |
| 409       | 750x600              | 334             | [409.jpg](.purrr_cache/409.jpg)       | [409.jpg](cats/409.jpg)     |
| 410       | 750x600              | 334             | [410.jpg](.purrr_cache/410.jpg)       | [410.jpg](cats/410.jpg)     |
| 411       | 750x600              | 334             | [411.jpg](.purrr_cache/411.jpg)       | [411.jpg](cats/411.jpg)     |
| 412       | 750x600              | 334             | [412.jpg](.purrr_cache/412.jpg)       | [412.jpg](cats/412.jpg)     |
| 413       | 750x600              | 334             | [413.jpg](.purrr_cache/413.jpg)       | [413.jpg](cats/413.jpg)     |
| 414       | 600x750              | 426             | [414.jpg](.purrr_cache/414.jpg)       | [414.jpg](cats/414.jpg)     |
| 415       | 750x600              | 334             | [415.jpg](.purrr_cache/415.jpg)       | [415.jpg](cats/415.jpg)     |
| 416       | 750x600              | 334             | [416.jpg](.purrr_cache/416.jpg)       | [416.jpg](cats/416.jpg)     |
| 417       | 750x600              | 334             | [417.jpg](.purrr_cache/417.jpg)       | [417.jpg](cats/417.jpg)     |
| 418       | 750x600              | 334             | [418.jpg](.purrr_cache/418.jpg)       | [418.jpg](cats/418.jpg)     |
| 421       | 750x600              | 334             | [421.jpg](.purrr_cache/421.jpg)       | [421.jpg](cats/421.jpg)     |
| 422       | 600x750              | 302             | [422.jpg](.purrr_cache/422.jpg)       | [422.jpg](cats/422.jpg)     |
| 423       | 750x600              | 334             | [423.jpg](.purrr_cache/423.jpg)       | [423.jpg](cats/423.jpg)     |
| 424       | 750x600              | 334             | [424.jpg](.purrr_cache/424.jpg)       | [424.jpg](cats/424.jpg)     |
| 425       | 750x600              | 334             | [425.jpg](.purrr_cache/425.jpg)       | [425.jpg](cats/425.jpg)     |
| 426       | 750x600              | 334             | [426.jpg](.purrr_cache/426.jpg)       | [426.jpg](cats/426.jpg)     |
| 428       | 750x600              | 333             | [428.jpg](.purrr_cache/428.jpg)       | [428.jpg](cats/428.jpg)     |
| 429       | 750x600              | 334             | [429.jpg](.purrr_cache/429.jpg)       | [429.jpg](cats/429.jpg)     |
| 431       | 750x600              | 334             | [431.jpg](.purrr_cache/431.jpg)       | [431.jpg](cats/431.jpg)     |
| 451       | 750x600              | 334             | [451.jpg](.purrr_cache/451.jpg)       | [451.jpg](cats/451.jpg)     |
| 500       | 750x600              | 334             | [500.jpg](.purrr_cache/500.jpg)       | [500.jpg](cats/500.jpg)     |
| 501       | 750x600              | 334             | [501.jpg](.purrr_cache/501.jpg)       | [501.jpg](cats/501.jpg)     |
| 502       | 750x600              | 334             | [502.jpg](.purrr_cache/502.jpg)       | [502.jpg](cats/502.jpg)     |
| 503       | 750x600              | 334             | [503.jpg](.purrr_cache/503.jpg)       | [503.jpg](cats/503.jpg)     |
| 504       | 750x600              | 334             | [504.jpg](.purrr_cache/504.jpg)       | [504.jpg](cats/504.jpg)     |
| 505       | 750x600              | 334             | [505.jpg](.purrr_cache/505.jpg)       | [505.jpg](cats/505.jpg)     |
| 506       | 750x600              | 334             | [506.jpg](.purrr_cache/506.jpg)       | [506.jpg](cats/506.jpg)     |
| 507       | 750x600              | 334             | [507.jpg](.purrr_cache/507.jpg)       | [507.jpg](cats/507.jpg)     |
| 508       | 750x600              | 334             | [508.jpg](.purrr_cache/508.jpg)       | [508.jpg](cats/508.jpg)     |
| 510       | 750x600              | 334             | [510.jpg](.purrr_cache/510.jpg)       | [510.jpg](cats/510.jpg)     |
| 511       | 750x600              | 334             | [511.jpg](.purrr_cache/511.jpg)       | [511.jpg](cats/511.jpg)     |

### Adapting Without Hardcoding
While hardcoding the frame border width (to skip every 1, 2 or more pixels in every step on the axis), vertices or margins might seem like the next logical step, this approach deliberately avoids it. Instead, by dynamically identifying the frame edges, the algorithm gracefully adapts to changes in picture resolution, ensuring robust and future-proof performance.

### A Note to Fellow Optimizers
The author is deeply curious about just how far we can push the limits of this algorithm. If you have insights or ideas for algorithmic improvements—or simply want to share a clever way to scan smarter—please reach out!
