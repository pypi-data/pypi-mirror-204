import { expect, test } from '@jest/globals';
import { VecSpaceClient } from '../src/index'
import vecspace from './initClient'

test('it should list collections', async () => {
    await vecspace.reset()
    let collections = await vecspace.listCollections()
    expect(collections).toBeDefined()
    expect(collections).toBeInstanceOf(Array)
    expect(collections.length).toBe(0)
    const collection = await vecspace.createCollection('test')
    collections = await vecspace.listCollections()
    expect(collections.length).toBe(1)
})

test('it should create a collection', async () => {
    await vecspace.reset()
    const collection = await vecspace.createCollection('test')
    expect(collection).toBeDefined()
    expect(collection).toHaveProperty('name')
    expect(collection.name).toBe('test')
    let collections = await vecspace.listCollections()
    expect([{ name: 'test', metadata: null }]).toEqual(expect.arrayContaining(collections));
    expect([{ name: 'test2', metadata: null }]).not.toEqual(expect.arrayContaining(collections));

    await vecspace.reset()
    const collection2 = await vecspace.createCollection('test2', { test: 'test' })
    expect(collection2).toBeDefined()
    expect(collection2).toHaveProperty('name')
    expect(collection2.name).toBe('test2')
    expect(collection2).toHaveProperty('metadata')
    expect(collection2.metadata).toHaveProperty('test')
    expect(collection2.metadata).toEqual({ test: 'test' })
    let collections2 = await vecspace.listCollections()
    expect([{ name: 'test2', metadata: { test: 'test' } }]).toEqual(expect.arrayContaining(collections2));

})

test('it should get a collection', async () => {
    await vecspace.reset()
    const collection = await vecspace.createCollection('test')
    const collection2 = await vecspace.getCollection('test')
    expect(collection).toBeDefined()
    expect(collection2).toBeDefined()
    expect(collection).toHaveProperty('name')
    expect(collection2).toHaveProperty('name')
    expect(collection.name).toBe(collection2.name)
})

test('it should get or create a collection', async () => {
    await vecspace.reset()
    await vecspace.createCollection('test')

    const collection2 = await vecspace.getOrCreateCollection('test')
    expect(collection2).toBeDefined()
    expect(collection2).toHaveProperty('name')
    expect(collection2.name).toBe('test')

    const collection3 = await vecspace.getOrCreateCollection('test3')
    expect(collection3).toBeDefined()
    expect(collection3).toHaveProperty('name')
    expect(collection3.name).toBe('test3')
})

test('it should delete a collection', async () => {
    await vecspace.reset()
    const collection = await vecspace.createCollection('test')
    let collections = await vecspace.listCollections()
    expect(collections.length).toBe(1)
    await vecspace.deleteCollection('test')
    collections = await vecspace.listCollections()
    expect(collections.length).toBe(0)
})

// TODO: I want to test this, but I am not sure how to
// test('custom index params', async () => {
//     throw new Error('not implemented')
//     await vecspace.reset()
//     const collection = await vecspace.createCollection('test', {"hnsw:space": "cosine"})
// })