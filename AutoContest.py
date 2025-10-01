#!/usr/bin/env python3
"""
AutoContest
Automated Sweepstakes & Contest Entry Tool

by Adam Rivers — A product of Hello Security LLC Research Labs
"""

import os
import json
import logging
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from urllib.parse import urljoin

# ========== Init ==========
console = Console()

CONFIG_FILE = "config.json"
RESULT_FILE = "contest-results.json"

# ========== Config ==========
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "aggregator_urls": [
                "https://www.sweepstakesfanatics.com/",
                "https://www.contestgirl.com/",
                "https://www.sweepsadvantage.com/",
                "https://www.winprizesonline.com/",
                "https://www.sweepstakestoday.com/",
                "https://online-sweepstakes.com/",
                "https://www.contestbee.com/",
                "https://thefreebieguy.com/current-sweepstakes-and-giveaways/",
                "https://www.pch.com/sweepstakes",
                "https://www.hgtv.com/sweepstakes",
                "https://people.com/sweepstakes",
                "https://www.realsimple.com/sweepstakes",
                "https://www.womansday.com/sweepstakes/",
                "https://www.bhg.com/sweepstakes/",
                "https://www.goodhousekeeping.com/sweepstakes/",
                "https://www.ellentube.com/sweepstakes.html",
                "https://www.travelchannel.com/sweepstakes",
                "https://www.foodnetwork.com/sponsored/sweepstakes",
                "https://www.oprah.com/sweepstakes",
                "https://www.parents.com/sweepstakes/",
                "https://www.instyle.com/sweepstakes",
                "https://www.countryliving.com/sweepstakes/",
                "https://www.redbookmag.com/sweepstakes/",
                "https://www.shape.com/sweepstakes",
                "https://www.southernliving.com/sweepstakes",
                "https://www.marthastewart.com/sweepstakes",
                "https://www.diynetwork.com/sweepstakes",
                "https://www.womansworld.com/sweepstakes",
                "https://www.rachaelraymag.com/sweepstakes",
                "https://www.leitesculinaria.com/sweepstakes",
                "https://www.tasteofhome.com/sweepstakes/",
                "https://www.usatoday.com/sweepstakes/",
                "https://www.luckysweeps.com/",
                "https://www.giveawayfrenzy.com/",
                "https://www.sweepon.com/",
                "https://www.gleam.io/discover/sweepstakes",
                "https://www.contestcorner.com/",
                "https://www.sweetiessweeps.com/",
                "https://www.infinitesweeps.com/",
                "https://www.giveawaypromote.com/",
                "https://www.sweepscheck.com/",
                "https://www.contestchest.com/",
                "https://www.sweepstakeslovers.com/",
                "https://www.giveawaymonkey.com/",
                "https://www.thebalanceeveryday.com/sweepstakes-and-contests-4685789",
                "https://www.siriusxm.com/sweepstakes",
                "https://www.iheart.com/sweepstakes/",
                "https://www.marieclaire.com/sweepstakes/",
                "https://www.cosmopolitan.com/sweepstakes/",
                "https://www.americanfamily.com/sweepstakes/",
                "https://www.anheuser-busch.com/sweepstakes",
                "https://www.coca-cola.com/en/offerings/sweepstakes",
                "https://www.pepsi.com/en-us/sweepstakes/",
                "https://www.toyota.com/usa/sweepstakes.html",
                "https://www.ford.com/sweepstakes/",
                "https://www.chevrolet.com/sweepstakes",
                "https://www.nissanusa.com/sweepstakes.html",
                "https://www.dell.com/en-us/giveaways",
                "https://www.intel.com/content/www/us/en/gaming/sweepstakes.html",
                "https://www.microsoft.com/en-us/store/b/sweepstakes",
                "https://www.amazon.com/b?node=14365911011",
                "https://ultracontest.com/",
                "https://www.sweepsatlas.com/",
                "https://prizegrab.com/",
                "https://giveawaylisting.com/",
                "https://www.bloggiveawaydirectory.com/",
                "https://contestwatchers.com/",
                "https://www.liveabout.com/sweepstakes-4163146",
                "https://www.ilovegiveaways.com/",
                "https://1sweepstakes.com/"
            ],
            "field_mappings": {
                "first_name": "first_name",
                "last_name": "last_name",
                "email": "email",
                "address": "address",
                "city": "city",
                "state": "state",
                "zip": "zip",
                "phone": "phone"
            },
            "user_data": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "example@email.com",
                "address": "123 Main St",
                "city": "Sampletown",
                "state": "CA",
                "zip": "12345",
                "phone": "1234567890"
            },
            "max_retries": 3,
            "twocaptcha_api_key": ""
        }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def get_user_data(config):
    if config.get("user_data"):
        console.print("[cyan]Using saved user details.[/]")
        return config["user_data"]
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "example@email.com",
        "address": "123 Main St",
        "city": "Sampletown",
        "state": "CA",
        "zip": "12345",
        "phone": "1234567890"
    }

def input_user_data():
    console.print(Panel.fit("[bold cyan]Enter Your Details[/]", border_style="cyan"))
    user_data = {}
    user_data["first_name"] = Prompt.ask("First Name", default="John")
    user_data["last_name"] = Prompt.ask("Last Name", default="Doe")
    user_data["email"] = Prompt.ask("Email", default="example@email.com")
    user_data["address"] = Prompt.ask("Address", default="123 Main St")
    user_data["city"] = Prompt.ask("City", default="Sampletown")
    user_data["state"] = Prompt.ask("State (e.g., CA)", default="CA")
    user_data["zip"] = Prompt.ask("Zip Code", default="12345")
    user_data["phone"] = Prompt.ask("Phone Number", default="1234567890")
    return user_data

def init_logging():
    logging.basicConfig(
        filename="automation.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def update_aggregator_urls(config):
    console.print(Panel.fit("[bold cyan]Automatically Updating Aggregator URLs[/]", border_style="cyan"))
    
    # Curated list of hub sites that list sweepstakes aggregators (no API needed)
    hub_sites = [
        "https://www.liveabout.com/best-sweepstakes-websites-4163145",
        "https://www.thebalanceeveryday.com/top-sweepstakes-directories-896784",
        "https://www.sweepstakeslovers.com/resources/",
        "https://www.contestgirl.com/links/"
    ]
    
    new_aggregators = []
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Discovering new aggregators...", total=len(hub_sites))
        for hub in hub_sites:
            try:
                resp = requests.get(hub, timeout=10)
                if resp.status_code >= 400:
                    progress.advance(task)
                    continue
                soup = BeautifulSoup(resp.text, "html.parser")
                links = [urljoin(hub, a["href"]) for a in soup.find_all("a", href=True) if a.get("href")]
                for link in links:
                    if not link.startswith("http") or link in config["aggregator_urls"]:
                        continue
                    try:
                        # Verify if the link is an aggregator by checking for multiple contest links
                        link_resp = requests.get(link, timeout=10)
                        if link_resp.status_code >= 400:
                            continue
                        link_soup = BeautifulSoup(link_resp.text, "html.parser")
                        contest_links = [a["href"] for a in link_soup.find_all("a", href=True) 
                                       if "sweep" in a["href"].lower() or "contest" in a["href"].lower() or "giveaway" in a["href"].lower()]
                        if len(contest_links) > 3:  # Threshold for aggregator-like sites
                            new_aggregators.append(link)
                            console.print(f"[green]Found new aggregator: {link}[/]")
                    except Exception as e:
                        logging.warning(f"Could not verify {link}: {e}")
                progress.advance(task)
            except Exception as e:
                logging.warning(f"Could not scrape hub {hub}: {e}")
                progress.advance(task)
    
    added = 0
    for url in new_aggregators:
        if url not in config["aggregator_urls"]:
            config["aggregator_urls"].append(url)
            added += 1
    save_config(config)
    console.print(f"[green]Added {added} new aggregator URLs to the list.[/]")

# ========== Scraping ==========
def scrape_contest_urls(aggregator_urls):
    urls = []
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Scraping contest URLs...", total=len(aggregator_urls))
        for agg in aggregator_urls:
            try:
                resp = requests.get(agg, timeout=10)
                soup = BeautifulSoup(resp.text, "html.parser")
                links = [urljoin(agg, a["href"]) for a in soup.find_all("a", href=True) if a.get("href")]
                urls.extend([l for l in links if l.startswith("http") and ("sweep" in l.lower() or "contest" in l.lower() or "giveaway" in l.lower())])
                progress.advance(task)
            except Exception as e:
                logging.warning(f"Could not scrape {agg}: {e}")
                progress.advance(task)
    return list(set(urls))

# ========== Form Submission ==========
async def submit_form_async(url, user_data, headers, field_mappings, retries, api_key):
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=15) as resp:
                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")
                    forms = soup.find_all("form")
                    if not forms:
                        return False, attempt, "No forms found"

                    form = forms[0]  # first form for demo
                    method = form.get("method", "post").lower()
                    inputs = form.find_all(["input", "select", "textarea"])
                    form_data = {}

                    # CAPTCHA detection and solving
                    recaptcha_div = soup.find("div", class_="g-recaptcha")
                    if recaptcha_div:
                        sitekey = recaptcha_div.get("data-sitekey")
                        if not sitekey:
                            return False, attempt, "CAPTCHA detected but no sitekey"
                        if not api_key:
                            return False, attempt, "CAPTCHA detected, no API key"
                        try:
                            from twocaptcha import TwoCaptcha
                        except ImportError:
                            return False, attempt, "2captcha library not installed"
                        solver = TwoCaptcha(api_key)
                        try:
                            loop = asyncio.get_event_loop()
                            result = await loop.run_in_executor(None, lambda: solver.recaptcha(sitekey=sitekey, url=url))
                            form_data['g-recaptcha-response'] = result['code']
                        except Exception as e:
                            return False, attempt, f"CAPTCHA solve failed: {str(e)}"

                    # hCaptcha detection
                    hcaptcha_div = soup.find("div", class_="h-captcha")
                    if hcaptcha_div:
                        sitekey = hcaptcha_div.get("data-sitekey")
                        if not sitekey:
                            return False, attempt, "hCAPTCHA detected but no sitekey"
                        if not api_key:
                            return False, attempt, "hCAPTCHA detected, no API key"
                        try:
                            from twocaptcha import TwoCaptcha
                        except ImportError:
                            return False, attempt, "2captcha library not installed"
                        solver = TwoCaptcha(api_key)
                        try:
                            loop = asyncio.get_event_loop()
                            result = await loop.run_in_executor(None, lambda: solver.hcaptcha(sitekey=sitekey, url=url))
                            form_data['h-captcha-response'] = result['code']
                        except Exception as e:
                            return False, attempt, f"hCAPTCHA solve failed: {str(e)}"

                    for i in inputs:
                        name = i.get("name")
                        if not name:
                            continue
                        if i.name == "input":
                            input_type = i.get("type", "text").lower()
                            if input_type in ("submit", "button", "image"):
                                continue
                            if input_type == "checkbox":
                                form_data[name] = i.get("value", "on")  # Auto-check checkboxes
                            elif input_type == "radio":
                                if name not in form_data:
                                    form_data[name] = i.get("value", "")
                            elif input_type == "hidden":
                                form_data[name] = i.get("value", "")
                            else:  # text, email, tel, etc.
                                if name in field_mappings:
                                    form_data[name] = user_data.get(field_mappings[name], "")
                                elif "email" in name.lower():
                                    form_data[name] = user_data["email"]
                                elif "first" in name.lower():
                                    form_data[name] = user_data["first_name"]
                                elif "last" in name.lower():
                                    form_data[name] = user_data["last_name"]
                                elif "phone" in name.lower():
                                    form_data[name] = user_data["phone"]
                                elif "address" in name.lower():
                                    form_data[name] = user_data["address"]
                                elif "city" in name.lower():
                                    form_data[name] = user_data["city"]
                                elif "state" in name.lower():
                                    form_data[name] = user_data["state"]
                                elif "zip" in name.lower():
                                    form_data[name] = user_data["zip"]
                                else:
                                    form_data[name] = "test"
                        elif i.name == "textarea":
                            form_data[name] = "N/A"
                        elif i.name == "select":
                            options = i.find_all("option")
                            if options:
                                for opt in options:
                                    if opt.get("value"):
                                        form_data[name] = opt["value"]
                                        break

                    action = urljoin(url, form.get("action") or "")

                    if method == "post":
                        async with session.post(action, data=form_data, headers=headers) as submit_resp:
                            text = await submit_resp.text()
                            if submit_resp.status < 400 or any(word in text.lower() for word in ["thank", "success", "entered", "submitted"]):
                                return True, attempt, "Submitted"
                            else:
                                return False, attempt, f"HTTP {submit_resp.status} - {text[:100]}"
                    elif method == "get":
                        async with session.get(action, params=form_data, headers=headers) as submit_resp:
                            text = await submit_resp.text()
                            if submit_resp.status < 400 or any(word in text.lower() for word in ["thank", "success", "entered", "submitted"]):
                                return True, attempt, "Submitted"
                            else:
                                return False, attempt, f"HTTP {submit_resp.status} - {text[:100]}"
                    else:
                        return False, attempt, f"Unsupported method: {method}"

        except Exception as e:
            logging.error(f"Error on {url}: {e}")
    return False, retries, "Failed after retries"

# ========== UI ==========
def display_banner():
    console.print(Panel.fit(
        "[bold cyan]🚀 AutoContest[/]\n[white]Automated Sweepstakes & Contest Entry Tool[/]\n\n"
        "[dim]by Adam Rivers — A product of Hello Security LLC Research Labs[/]",
        border_style="cyan",
        title="Welcome",
        subtitle="Automation Ready"
    ))

def display_results(results, start_time, result_file):
    table = Table(show_lines=True, header_style="bold magenta", border_style="cyan")
    table.add_column("Site", style="cyan", overflow="fold")
    table.add_column("Result", justify="center", style="bold")
    table.add_column("Notes", justify="left", style="white")

    for r in results:
        url = f"[cyan]{r['url']}[/]"
        if r["submitted"]:
            result = "[green]Success[/]"
            notes = f"{r.get('forms', 1)} form(s) attempted"
        elif "CAPTCHA" in r["reason"]:
            result = "[yellow]Skipped (CAPTCHA)[/]"
            notes = "CAPTCHA detected"
        elif "No forms" in r["reason"]:
            result = "[yellow]Skipped (no forms)[/]"
            notes = "No form elements found"
        else:
            result = "[red]Failed[/]"
            notes = r["reason"]
        table.add_row(url, result, notes)

    console.print(Panel.fit("[bold cyan]📊 Contest Automation Summary[/]", border_style="cyan"))
    console.print(table)

    total = len(results)
    success = sum(r["submitted"] for r in results)
    duration = (datetime.now() - start_time).total_seconds()

    console.print(
        Panel.fit(
            f"[bold green]Automation complete — {success}/{total} sites in {duration:.1f}s[/]\n\n"
            f"[white]Results saved to:[/] [magenta]{result_file}[/]",
            border_style="green"
        )
    )

# ========== Main Automation ==========
async def run_automation_async(update_aggregators=False):
    config = load_config()
    if update_aggregators:
        update_aggregator_urls(config)
    user_data = get_user_data(config)
    start_time = datetime.now()
    contest_urls = scrape_contest_urls(config["aggregator_urls"])

    results = []
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Submitting forms...", total=len(contest_urls))
        for url in contest_urls:
            try:
                result = await submit_form_async(
                    url, user_data, {"User-Agent": "Mozilla/5.0"},
                    config["field_mappings"], config["max_retries"], config["twocaptcha_api_key"]
                )
                results.append({
                    "url": url,
                    "submitted": result[0],
                    "retries": result[1],
                    "reason": result[2],
                    "forms": 1
                })
                progress.advance(task)
            except Exception as e:
                results.append({"url": url, "submitted": False, "retries": 0, "reason": f"Error: {str(e)}"})
                progress.advance(task)

    with open(RESULT_FILE, "w") as f:
        json.dump(results, f, indent=4)

    display_results(results, start_time, RESULT_FILE)

def run_automation(update_aggregators=False):
    asyncio.run(run_automation_async(update_aggregators))

# ========== Menu ==========
def menu():
    display_banner()
    config = load_config()
    while True:
        console.print(Panel.fit(
            "[1] Run Automation\n[2] View Last Results\n[3] Enter User Details\n[4] Update Aggregator URLs\n[5] Exit",
            title="[bold cyan]Main Menu[/]", border_style="cyan"
        ))
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"])
        if choice == "1":
            run_automation(update_aggregators=True)
        elif choice == "2":
            if os.path.exists(RESULT_FILE):
                with open(RESULT_FILE, "r") as f:
                    results = json.load(f)
                display_results(results, datetime.now(), RESULT_FILE)
            else:
                console.print("[red]No results found. Run automation first.[/]")
        elif choice == "3":
            config["user_data"] = input_user_data()
            save_config(config)
            console.print("[green]User details saved successfully![/]")
        elif choice == "4":
            update_aggregator_urls(config)
        elif choice == "5":
            console.print("[yellow]Exiting AutoContest...[/]")
            break

if __name__ == "__main__":
    init_logging()
    menu()
