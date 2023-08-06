import { expect, test } from '@jest/globals';
import { VecSpaceClient } from '../src/index'
import vecspace from './initClient'

test('it should create the client connection', async () => {
    expect(vecspace).toBeDefined()
    expect(vecspace).toBeInstanceOf(VecSpaceClient)
})

test('it should get the version', async () => {
    const version = await vecspace.version()
    expect(version).toBeDefined()
    expect(version).toMatch(/^[0-9]+\.[0-9]+\.[0-9]+$/)
})

test('it should get the heartbeat', async () => {
    const heartbeat = await vecspace.heartbeat()
    expect(heartbeat).toBeDefined()
    expect(heartbeat).toBeGreaterThan(0)
})

test('it should reset the database', async () => {
    await vecspace.reset()
    const collections = await vecspace.listCollections()
    expect(collections).toBeDefined()
    expect(collections).toBeInstanceOf(Array)
    expect(collections.length).toBe(0)
    
    const collection = await vecspace.createCollection('test')
    const collections2 = await vecspace.listCollections()
    expect(collections2).toBeDefined()
    expect(collections2).toBeInstanceOf(Array)
    expect(collections2.length).toBe(1)
    
    await vecspace.reset()
    const collections3 = await vecspace.listCollections()
    expect(collections3).toBeDefined()
    expect(collections3).toBeInstanceOf(Array)
    expect(collections3.length).toBe(0)
})
