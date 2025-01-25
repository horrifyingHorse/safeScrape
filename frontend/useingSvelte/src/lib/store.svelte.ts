import { get, writable, type Writable } from "svelte/store"

export interface PageState {
  auto_login: boolean,
  storage_state: string,
  service: string,
  custom_url: string,
  scrape: boolean,
  allow_delay: boolean,
  execute: boolean
}

class PgState {
  public pageState: PageState[] = $state([{
    auto_login: false,
    new_state: false,
    storage_state: "",
    service: "",
    custom_url: "",
    scrape: false,
    allow_delay: true,
    execute: false,
  }])
  public pageId: number = $state(0)

  public update(id: number, state: PageState) {
    this.pageId = id
    this.pageState[0] = state
  }

  public toggleAutoLogin = () => {
    this.pageState[0].auto_login = !this.pageState[0].auto_login
  }

  public toggleAllowDelay = () => {
    this.pageState[0].allow_delay = !this.pageState[0].allow_delay
  }
}

// Singleton
class PageInstances {
  private static instance: PageInstances | null = null
  public instanceStore: { [key: number]: string } = {}
  public iterableInstanceStore: string[] = $state([])

  private constructor() { }

  public static getManager() {
    if (PageInstances.instance === null) {
      PageInstances.instance = new PageInstances()
    }
    return PageInstances.instance
  }

  public addInstance(id: number, name: string) {
    this.instanceStore[id] = name
    this.createIterable()
  }

  public instanceCount(): number {
    return this.iterableInstanceStore.length
  }

  public clear() {
    this.iterableInstanceStore = []
    this.instanceStore = {}
  }

  private createIterable() {
    let newIterable: string[] = []
    for (let idx in this.instanceStore) {
      newIterable[idx] = `#${idx}:${this.instanceStore[idx]}`
    }
    this.iterableInstanceStore = newIterable
  }
}

export const pgState: PgState = new PgState()
export const services: Writable<string[]> = writable<string[]>([])
export const storageStates: Writable<string[]> = writable<string[]>(["default"])
export const pgInstances: PageInstances = PageInstances.getManager()
export const stateName: Writable<string> = writable<string>("template");
export const newStateWanted: Writable<boolean> = writable<boolean>(false);

class Display {
  private displayDiv: HTMLDivElement | null = null
  private taskId: number = 0

  constructor(id: string | null) {
    if (id === null) return
    this.displayDiv = (document.getElementById(id) as HTMLDivElement)
  }

  public init(id: string | null) {
    if (this.displayDiv !== null) {
      console.error("A div has already been assigned displayDiv")
      return
    }
    if (id === null) {
      this.displayDiv = null
      return
    }
    this.displayDiv = (document.getElementById(id) as HTMLDivElement)
  }

  public log(msg: string, classList: string[] = []) {
    if (this.displayDiv === null) return
    const child = this.createChildDiv(msg, classList)
    let lastChild: HTMLDivElement | null = null
    if (this.displayDiv.children.length > 2) {
      lastChild = this.displayDiv.children[this.displayDiv.children.length - 1] as HTMLDivElement;
    }
    this.displayDiv.appendChild(child)
    if (lastChild && (lastChild.getClientRects() as DOMRectList)[0].top <= window.innerHeight) {
      child.scrollIntoView(false)
    }
  }

  public success(msg: string, classList: string[] = []) {
    this.log(msg, [...classList, "text-lime-400"])
  }

  public serverlog(msg: string, classList: string[] = []) {
    this.log(msg, [...classList, "text-yellow-400"])
  }

  public error(msg: string, classList: string[] = []) {
    this.log(msg, [...classList, "text-red-400"])
  }

  private createChildDiv(msg: string, classList: string[] = []): HTMLDivElement {
    const div = document.createElement("div")
    const timeSpan = this.createTime()
    const msgSpan = document.createElement("span")
    if (classList.length) {
      msgSpan.classList.add(...classList)
    }
    msgSpan.innerText = ` ${msg}`
    div.appendChild(timeSpan)
    div.appendChild(msgSpan)
    return div
  }

  private createTime(): HTMLSpanElement {
    const timeSpan = document.createElement("span")
    timeSpan.classList.add("select-none", "text-zinc-400")
    timeSpan.innerText = `[${Date().split(" ")[4]}]`
    return timeSpan
  }
}
export const logDisplay: Display = new Display(null)

export interface ScrapedData {
  MsgId: number,
  ReplyTo: string | null,
  Author: string,
  Content: string,
}

export let indexedDataBaseNames: string[] = []
export const SockConn: Writable<WebSocket | null> = writable(null)
export async function upSockConn(ws_addr: number) {
  SockConn.update((ws: WebSocket | null) => {
    if (ws !== null) {
      ws.close()
    }
    indexedDataBaseNames.push(`${ws_addr}`)
    return new WebSocket(`ws://localhost:8000/scrapy/${ws_addr}`)
  })

  const newSockConn = get(SockConn);
  if (!newSockConn) return
  newSockConn.onopen = () => {
    logDisplay.success("Connected to " + newSockConn.url)
  }
  newSockConn.onmessage = (event) => {
    const data: ScrapedData[] = JSON.parse(event.data)
    console.log(data)

    const indexedDB = window.indexedDB.open(`${ws_addr}`)
    let db: null | IDBDatabase

    indexedDB.onerror = () => {
      console.error("already exists")
    }
    indexedDB.onupgradeneeded = () => {
      const db = indexedDB.result
      if (db.objectStoreNames.contains("msgs")) return
      const objStore = db.createObjectStore("msgs", { keyPath: "MsgId", })
      objStore.createIndex("Author", "Author", { unique: false })
      objStore.createIndex("ReplyTo", "ReplyTo", { unique: false })
      objStore.createIndex("Content", "Content", { unique: false })
    }
    indexedDB.onsuccess = () => {
      db = indexedDB.result
      console.log("created")
      const transaction = db.transaction("msgs", "readwrite")
      transaction.onerror = () => console.error("Transaction failed")
      const msgs = transaction.objectStore("msgs")

      data.forEach(item => {
        const request = msgs.add(item)
        request.onsuccess = () => console.log("Written")
        request.onerror = () => console.log("Failed to write")
      })
      db.close()
    }
  }
}
