import { writable } from "svelte/store"

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

export class PageInstances {
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
export const services = writable<string[]>([])
export const storageStates = writable<string[]>([])
export const pgInstances: PageInstances = PageInstances.getManager()
