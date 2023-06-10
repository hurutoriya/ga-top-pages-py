from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from datetime import datetime, timedelta
import frontmatter
import argparse


def get_top_pages_report(property_id: str, site_content_path: str, pages_root_url:str, top_n: int):
    """
    Show Top N page report with markdown format from one year ago based on
    Google Analytics result.

    Args:
        property_id (str): Google Analytics(GA4) property_id
        site_content_path (str): static site generator content root path
        pages_root_url (str): pages root URL. e.g. https://shunyaueta.com to generate each page URL. Please remove / in end of URL if you have that.
        top_n (int): extract top N post based on aggregated result
    """

    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()
    # Get 1 year ago date
    one_year_ago = datetime.now() - timedelta(days=365)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="totalUsers")],
        date_ranges=[
            DateRange(start_date=one_year_ago.strftime("%Y-%m-%d"), end_date="today")
        ],
    )
    response = client.run_report(request)

    print(f"## 直近一年間の人気記事 Top{top_n} \n")

    for row in response.rows[: top_n + 1]:
        # Exclude a root page since always root page is included with in top 10 pages
        if row.dimension_values[0].value != "/":
            view_cnt = row.metric_values[0].value
            page_path = row.dimension_values[0].value
            page_title = get_page_title(
                page_path=page_path, site_content_path=site_content_path
            )
            print(f"1. `{view_cnt}` views: [{page_title}]({pages_root_url + page_path})")


def get_page_title(page_path: str, site_content_path: str) -> str:
    """
    Get page title in frontmatter

    Args:
        page_path (str): page path to markdown file
        site_content_path (str): static site generator content root path

    Returns:
        str: markdown file path
    """

    # Convert to Markdown file path
    markdown_file_path = site_content_path + page_path + "index.md"
    # Read file and get frontmatter
    with open(markdown_file_path, "r") as file:
        content = file.read()
        post = frontmatter.loads(content)

    return post["title"]


if __name__ == "__main__":
    # NOTE: support command option
    parser = argparse.ArgumentParser(
        description="Generate top pages report based on Google Analytics(GA4) for Static Site Generator"
    )
    parser.add_argument("-property_id", type=str, help="Property ID")
    parser.add_argument(
        "-site_content_path",
        type=str,
        help="Path to site content in static site generator(e.g. Hugo)",
    )
    parser.add_argument("-pages_root_url", type=str, help="pages_root_url e.g. https://shunyaueta.com")
    parser.add_argument("-top_n", type=int, help="Number of top pages to retrieve")

    args = parser.parse_args()

    get_top_pages_report(
        property_id=args.property_id,
        site_content_path=args.site_content_path,
        pages_root_url=args.pages_root_url,
        top_n=args.top_n,
    )
